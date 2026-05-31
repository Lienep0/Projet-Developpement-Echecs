#include <cstdio>
#include "Module.cu"
#include <cstdlib>
#include <cublas.h>

//with padding and stride
__global__ void conv2d( float* input, float* output, float* weights, float* bias, int in_channels, int out_channels, int kernel_height, int kernel_width, int input_width, int input_height,int stride, int padding) {
	int i = blockIdx.x * blockDim.x + threadIdx.x;
	int j = blockIdx.y * blockDim.y + threadIdx.y;
	int k = blockIdx.z * blockDim.z + threadIdx.z;

	int out_Height = 1 + int((input_height - kernel_height + 2 * padding) / stride);
	int out_Width = 1 + int((input_width - kernel_width + 2 * padding) / stride);

	float sum = 0.0f;

	if (i >= out_Height || j >= out_Width || k >= out_channels) return;//bound check

	for(int ic=0; ic<in_channels; ic++) {
		// Implementation for each input channel
		for (int m = 0; m < kernel_height; m++) {
			for (int n = 0; n < kernel_width; n++) {
				// Calculate the convolution for the current position
				int input_x = stride * i+m;
				int input_y = stride * j+n;
				if (input_x >= 0 && input_x < input_width && input_y >= 0 && input_y < input_height) {
					sum+= input[ic * input_width * input_height + input_y * input_width + input_x] *
						weights[k*kernel_height*kernel_width*in_channels + ic * kernel_height * kernel_width + m * kernel_height + n];
				}
			}
		}
	}

	output[i * out_Height + j + k * out_Height * out_Width] = sum + bias[k];
}

class Conv2D : public Module {
private:
	int in_channels;
	int out_channels;
	int* kernel_size;

	//No implementation of different size of stride and padding as Loukka uses int stride and padding
	int stride;
	int padding; 

	//No dilation used as Loukka does not use it, but it can be added later if needed
	Tensor weights;
	Tensor bias;
public:

	Conv2D(int in_channels, int out_channels, int kernel_size, int stride, int padding) :
		in_channels(in_channels), out_channels(out_channels), kernel_size(new int[2] {kernel_size, kernel_size}),
		weights(new int[4] {out_channels, in_channels, this->kernel_size[0], this->kernel_size[1]}, 4),
		bias(new int[1] {out_channels}, 1), stride(stride), padding(padding) {

	}
	void forward(Tensor& input, Tensor& output) {
		conv2d << <(out_channels * (input.dimensions[2] - kernel_size[0] + 1) * (input.dimensions[3] - kernel_size[1] + 1) + 255) / 256, 256 >> > (
			input.dev_data, output.dev_data, weights.dev_data, bias.dev_data,
			in_channels, out_channels, kernel_size, input.dimensions[3], input.dimensions[2]
			);
	
		cudaDeviceSynchronize();

		cudaMemcpy(output.data, output.dev_data, output.nbEle * sizeof(float), cudaMemcpyDeviceToHost);

	}

	void backward(Tensor& input, Tensor& gradOutput) {
		// Implement the backward pass to compute gradients for weights and bias
		// This is a placeholder implementation



	}


};
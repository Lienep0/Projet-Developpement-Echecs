#pragma once
#include <functional>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include "Module.cu"


using namespace std;

__global__ void multiply21(float* dev_data_a, float* dev_datab, float* dev_data_result, int dimensions1_a, int strides_a_0, int strides_a_1, int strides_b_0) {
	//Assuming it's 2d*1D (a*b)
	printf("beginning to multiply 2D and 1D tensors in kernel with thread %d\n", threadIdx.x);
	dev_data_result[threadIdx.x] = 0;
	for (int j = 0; j < dimensions1_a; j++) {
		dev_data_result[threadIdx.x] += dev_data_a[threadIdx.x * strides_a_0 + j * strides_a_1] * dev_datab[j * strides_b_0];
	}
	
}


__global__ void addd(float* dev_data_a, float* dev_data_b, float* dev_data_result) {
	//Assuming it's 1D+1D (a+b)
	dev_data_result[threadIdx.x] = dev_data_a[threadIdx.x] + dev_data_b[threadIdx.x];
}

class Linear :  public Module{
	private:
	Tensor weights;
public:

	Tensor bias;
	Linear(int input_size, int output_size) {
		cout << "Initializing layer with input size " << input_size << " and output size " << output_size << endl;
		int weights_dimension[] = {output_size, input_size};
		int bias_dimension[] = { output_size };

		
		this->weights = Tensor(weights_dimension, 2);
		cout << "Initialized weights tensor :[" << weights.dimensions[0] << ", " << weights.dimensions[1] << "]" << endl;

		this->bias = Tensor(bias_dimension, 1);
	}


	Linear() {
		this->weights = Tensor();
		this->bias = Tensor(); 
	}


	~Linear() {
		//The tensors will be automatically freed when the layer is destroyed
	}



	void forward(const Tensor& input, Tensor& output) {
		cout << "device forward called with input dimensions: " << input.dimensions[0] << " and output dimensions: " << output.dimensions[0] << endl;
		cout << output.dimensions[0] << " " << output.ndim << endl;
		cout << bias.dimensions[0] << " " << bias.ndim << endl;
		Tensor result(output.dimensions, output.ndim);
		cout << "Launching kernel with " << this->weights.dimensions[0] << " threads" << endl;
		multiply21<<<1, bias.dimensions[0]>>>(weights.dev_data, input.dev_data, result.dev_data, weights.dimensions[1], weights.strides[0], weights.strides[1], bias.strides[0]);
		cudaDeviceSynchronize();
		cout << "Finished multiplying, now adding bias" << endl;
		addd<<<1, bias.dimensions[0]>>>(result.dev_data, this->bias.dev_data, output.dev_data);
		cudaDeviceSynchronize();

		cudaMemcpy(output.data, output.dev_data, output.nbEle * sizeof(float), cudaMemcpyDeviceToHost);
	}

	void gradW(const Tensor& input, const Tensor& grad_output, Tensor& grad_weights) {

	}

	void gradB(const Tensor& input, const Tensor& grad_output, Tensor& grad_bias) {
	
	}

	void gradI(const Tensor& input, const Tensor& grad_output, Tensor& grad_input) {

	}

	void backward(const Tensor& input, const Tensor& grad_output, Tensor& grad_input) {
		
	}


};
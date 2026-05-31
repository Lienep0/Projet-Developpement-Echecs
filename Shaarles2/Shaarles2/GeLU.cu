#include <cstdio>
#include "Tensor.cu"
#include <cstdlib>
#include "Module.cu"

using namespace std;

__global__ void tanh(float* input, float* output, int n) {
	int idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx < n) {
		output[idx] = tanhf(input[idx]);
	}
}

__global__ void sqrt(float* input, float* output, int n) {
	int idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx < n) {
		output[idx] = sqrtf(input[idx]);
	}
}

__global__ void gelu(float* input, float* output, int n) {
	int idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx < n) {
		float x = input[idx];
		output[idx] = 0.5f * x * (1.0f + tanhf(0.79788456f * (x + 0.044715f * x * x * x)));
	}
}

class GeLU : public Module {
private:
	Tensor input;

public:

	Tensor forward(Tensor input) override {
		this->input = input.copy();
		Tensor output(input.dimensions, input.ndim);
		int blockSize = 256;
		int numBlocks = (input.nbEle + blockSize - 1) / blockSize;
		gelu<<<numBlocks, blockSize>>>(input.dev_data, output.dev_data, input.nbEle);
		cudaError_t c_err = cudaMemcpy(output.data, output.dev_data, input.nbEle * sizeof(float), cudaMemcpyDeviceToHost);
		if (c_err != cudaSuccess) {
			std::cerr << "cudaMemcpy failed: " << cudaGetErrorString(c_err) << std::endl;
		}
		return output;
	}

	void backward(Tensor input,Tensor gradOutput) override {
		Tensor gradInput(input.dimensions, input.ndim);
		int blockSize = 256;
		int numBlocks = (input.nbEle + blockSize - 1) / blockSize;
		sqrt<<<numBlocks, blockSize>>>(input.dev_data, gradInput.dev_data, input.nbEle);
		cudaError_t c_err = cudaMemcpy(gradInput.data, gradInput.dev_data, input.nbEle * sizeof(float), cudaMemcpyDeviceToHost);
		if (c_err != cudaSuccess) {
			std::cerr << "cudaMemcpy failed: " << cudaGetErrorString(c_err) << std::endl;
		}

		gradOutput = gradInput.copy();
	}	
};

#include <cstdio>
#include "Tensor.cu"
#include <cstdlib>
#include "Module.cu"

using namespace std;

class ReLU : public Module {
private:
	Tensor mask; //sert à stocker les mask pour la rétropagation
public:


	Tensor forward(Tensor input) override {
		// Implement the forward pass using the weights and bias
		// This is a placeholder implementation
		Tensor output(input.dimensions, input.ndim);
		mask = Tensor(input.dimensions, input.ndim); // Initialize the mask tensor with the same dimensions as input
		float value = 0.0f;
		
		reluForwardKernel << <(input.dimensions[0] * input.dimensions[1] + 255) / 256, 256 >> > (input.dev_data, output.dev_data, mask.dev_data, input.dimensions[0] * input.dimensions[1]);

		return output;
	}
	void backward(Tensor input, Tensor gradOutput) override {
		reluBackwardKernel << <(gradOutput.dimensions[0] * gradOutput.dimensions[1] + 255) / 256, 256 >> > (gradOutput.dev_data, mask.dev_data, input.dev_data, gradOutput.dimensions[0] * gradOutput.dimensions[1]);
	}
};

__global__ void reluForwardKernel(float* input, float* output, float* mask, int size) {
	int idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx < size) {
		float value = input[idx];
		if (value > 0) {
			output[idx] = value;
			mask[idx] = 1.0f; // Mark as active
		} else {
			output[idx] = 0.0f;
			mask[idx] = 0.0f; // Mark as inactive
		}
	}
}

__global__ void reluBackwardKernel(float* gradOutput, float* mask, float* gradInput, int size) {
	int idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx < size) {
		gradInput[idx] = gradOutput[idx] * mask[idx]; // Only propagate gradients for active neurons
	}
}
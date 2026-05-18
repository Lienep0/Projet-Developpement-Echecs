#include <cstdio>
#include "Tensor.cu"
#include <cstdlib>
#include "Module.cu"

using namespace std;


__global__ void reluForwardKernel(float* input, float* output, float* mask, int size) {
	int idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx < size) {
		float value = input[idx];
		if (value > 0) {
			output[idx] = value;
			mask[idx] = 1.0f; // Mark as active
			
		}
		else {
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

class ReLU : public Module {
private:
	Tensor mask; //sert à stocker les mask pour la rétropagation

public:


	Tensor forward(Tensor input) override {
		// Implement the forward pass using the weights and bias
		// This is a placeholder implement ation
		Tensor output(input.dimensions, input.ndim); // Create an output tensor with the same dimensions as input

		new (&mask) Tensor(input.dimensions, input.ndim); // Create a mask tensor with the same dimensions as input
		int vec_size = 1;
		for (int i = 0; i < input.ndim; i++) {
			vec_size = vec_size * input.dimensions[i];
		}


		
		cudaError_t c_err = cudaMemcpy(input.dev_data, input.data, vec_size * sizeof(float), cudaMemcpyHostToDevice);
		if (c_err != cudaSuccess) {
			std::cerr << "cudaMemcpy failed: " << cudaGetErrorString(c_err) << std::endl;
		}
		reluForwardKernel << <(vec_size + 255) / 256, 256 >> > (input.dev_data, output.dev_data, this->mask.dev_data, vec_size);
		
		cudaDeviceSynchronize();
		c_err = cudaMemcpy(output.data, output.dev_data, vec_size * sizeof(float), cudaMemcpyDeviceToHost);                                                                                                                                                                                                                                                                                        

		if (c_err != cudaSuccess) {
			std::cerr << "cudaMemcpy failed for output data: " << cudaGetErrorString(c_err) << std::endl;
		}


		//veryfing the mask values
		c_err = cudaMemcpy( (this->mask).data, (this->mask).dev_data, vec_size * sizeof(float), cudaMemcpyDeviceToHost);
		if (c_err != cudaSuccess) {
			std::cerr << "cudaMemcpy failed for mask copy from device to host: " << cudaGetErrorString(c_err) << std::endl;
		}

		return output;
	}
	void backward(Tensor input, Tensor gradOutput) override {
		int vec_size = 1;
		for (int i = 0; i < gradOutput.ndim; i++) {
			vec_size = vec_size * gradOutput.dimensions[i];
		}
		reluBackwardKernel << <(vec_size + 255) / 256, 256 >> > (gradOutput.dev_data, mask.dev_data, input.dev_data, vec_size);
	}

	void forwardd(Tensor input) override {
		// Implement the forward pass using the weights and bias on device
	}

	void backwardd(Tensor input, Tensor gradOutput) override {
		// Implement the backward pass to compute gradients for weights and bias on device
	}

	vector<Tensor*> parameters() override {
		// Return the parameters of the module (weights and bias)
		// This is a placeholder implementation
		vector<Tensor*> outputVec = {&mask};
		return outputVec;
	}

	Tensor getMask() {
		return mask;
	}
}                                                                  ;

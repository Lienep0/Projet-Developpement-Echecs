#include "Tensor.cu"
#include <cstdio>
#include <cstdlib>
#include <functional>


class Layer {
private:
	Tensor weights;
	Tensor bias;
	function<Tensor(Tensor)> activation; // Activation function for forward pass
	function<void(float*)> activationd; // Activation function for forward pass on device

public:
	void forward(Tensor input) {
		// Implement the forward pass using the weights and bias
		// This is a placeholder implementation
		Tensor output; // Compute the output based on input, weights, and bias
	}

	void forwardd(Tensor input) {
		// Implement the forward pass using the weights and bias on device
	}

	void backward(Tensor input, Tensor gradOutput) {
		// Implement the backward pass to compute gradients for weights and bias
		// This is a placeholder implementation
	}

	void backwardd(Tensor input, Tensor gradOutput) {
		// Implement the backward pass to compute gradients for weights and bias on device
	}



	void changeActivation(function<Tensor(Tensor)> newActivation) {
		this->activation = newActivation;
	}
	void changeActivations(function<void(float* )> newActivation) {
		this->activationd = newActivation;
	}
};


Tensor relu(Tensor input) {
	Tensor result(input.dimensions, input.ndim);
	for (int i = 0; i < input.dimensions[0]; i++) {
		result.data[i] = max(0.0f, input.data[i * input.strides[0]]);
	}
	return result;
}

__global__ void relud(float* input) {
	printf("Thread %d: Original value: %f\n", threadIdx.x, input[threadIdx.x]);
	input[threadIdx.x] = max(0.0f, input[threadIdx.x]);
}
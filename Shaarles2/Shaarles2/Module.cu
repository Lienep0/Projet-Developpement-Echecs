#include "Tensor.cu"
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <functional>


class Module {
private:
	bool training = true;

public:
	virtual Tensor forward(Tensor input) {
		// Implement the forward pass using the weights and bias
		// This is a placeholder implementation
		return Tensor();
	}

	virtual void forwardd(Tensor input) {
		// Implement the forward pass using the weights and bias on device
	}

	virtual void backward(Tensor input, Tensor gradOutput) {
		// Implement the backward pass to compute gradients for weights and bias
		// This is a placeholder implementation
	}

	virtual void backwardd(Tensor input, Tensor gradOutput) {
		// Implement the backward pass to compute gradients for weights and bias on device
	}

	virtual vector<Tensor*> parameters() {
		// Return the parameters of the module (weights and bias)
		// This is a placeholder implementation
		return vector<Tensor*>();
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
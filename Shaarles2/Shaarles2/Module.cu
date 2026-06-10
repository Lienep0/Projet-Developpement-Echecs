#include "Tensor.cu"
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <functional>


class Module {
protected://enables access to derived classes -> had problem when it was private in  BatchNorm2D where it's particularly useful so :(
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

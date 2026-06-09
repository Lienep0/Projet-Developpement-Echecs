#include <cstdio>
#include <cstdlib>
#include "Module.cu"

class BatchNorm2D : public Module {

private:
	//channel should always be one?
	//used only in inference
	Tensor running_mean;
	Tensor running_var;

	//used both in inference and training
	Tensor gamma;
	Tensor beta;


	//used only in training
	Tensor batch_mean;
	Tensor batch_var;
public:	
	
	BatchNorm2D(int num_features) {
	// Initialize weights and bias
	}
	Tensor forward(Tensor input) override {
		// Implement the forward pass for batch normalization
		Tensor output(input.dimensions, input.ndim); // Create an output tensor with the same dimensions as input
		if (training) {
			// Compute mean and variance for the current batch
			// Normalize the input using the computed mean and variance
		}
		else {
			// Use running mean and variance for normalization during inference
		}
		return output;
	}

	void backward(Tensor input, Tensor gradOutput) override {
		// Implement the backward pass to compute gradients for weights and bias
	}

};
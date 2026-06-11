#include <cstdlib>
#include <cstdio>

#include "Conv2D.cu"

int main() {
	// Example usage of the Conv2D module
	int dimensions[] = { 4, 4 ,2}; // Example dimensions for a 4x4 tensor
	Tensor input(dimensions, 3); // Create an input tensor with the specified dimensions
	Tensor output(dimensions, 3); // Create an output tensor to hold the results
	// Fill the input tensor with some values (for testing)
	for (int i = 0; i < 32; i++) {
		input.getData()[i] = static_cast<float>(i - 8); // Values from -8 to 7
		printf("element %d: %f\n", i, input.getData()[i]);
	}

	Conv2D conv2dModule(2, 2, 3, 1, 0); // Create an instance of the Conv2D module

	//expliciting the weights
	for (int i = 0; i < conv2dModule.weights.getnbEle(); i++) {
		conv2dModule.weights.getData()[i] = static_cast<float>(i - 4); // Values from -4 to 3
		printf("weight element %d: %f\n", i, conv2dModule.weights.getData()[i]);
	}
	conv2dModule.forward(input,2, dimensions[0], dimensions[1], output); // Perform the forward pass
	// Print the output tensor values

	//expliciting the weights
	for (int i = 0; i < conv2dModule.weights.getnbEle(); i++) {
		conv2dModule.weights.getData()[i] = static_cast<float>(i - 4); // Values from -4 to 3
		printf("weight element %d: %f\n", i, conv2dModule.weights.getData()[i]);
	}

	printf("Output after Conv2D	:\n");
	for (int i = 0; i < 32; i++) {
		printf("element %d: ", i);
		printf("%f ", output.getData()[i]);
		if ((i + 1) % 4 == 0) {
			printf("\n");
		}
	}

	return 0;
}
#include <cstdlib>
#include <cstdio>

#include "ReLU.cu"

int main() {
	// Example usage of the ReLU module
	int dimensions[] = { 4, 4 }; // Example dimensions for a 4x4 tensor
	Tensor input(dimensions, 2); // Create an input tensor with the specified dimensions
	Tensor output(dimensions,2); // Create an output tensor to hold the results
	// Fill the input tensor with some values (for testing)
	for (int i = 0; i < 16; i++) {
		input.data[i] = static_cast<float>(i - 8); // Values from -8 to 7
		printf("element %d: %f\n", i, input.data[i]);
	}

	ReLU reluModule; // Create an instance of the ReLU module
	output=reluModule.forward(input); // Perform the forward pass
	// Print the output tensor values
	printf("Output after ReLU activation:\n");
	for (int i = 0; i < 16; i++) {
		printf("element %d: ", i);
		printf("%f ", output.data[i]);
		if ((i + 1) % 4 == 0) {
			printf("\n");
		}
	}
	
	printf("Mask values after forward pass:\n");
	Tensor mask_relu = reluModule.getMask(); // Get the mask tensor from the ReLU module
	for (int i = 0; i < 16; i++) {
		printf("element %d: ", i);
		printf("%f ", mask_relu.data[i]);
		if ((i + 1) % 4 == 0) {
			printf("\n");
		}
	}
	return 0;
}
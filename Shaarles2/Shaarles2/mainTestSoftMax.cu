#include "SoftMax.cu"

int main() {
	// Define the dimensions of the input tensor (batch_size, channels, height, width)
	int dimensions[4] = { 1, 2, 4, 4 }; // Example dimensions
	// Create an input tensor with the specified dimensions
	Tensor input(dimensions, 3); // Create an input tensor to hold the data
	// Fill the input tensor with some values (for testing)
	for (int i = 0; i < 32; i++) {
		input.getData()[i] = static_cast<float>(i - 16); // Values from -16 to 15
		printf("element %d: %f\n", i, input.getData()[i]);
	}
	SoftMax softmaxModule(2); // Create an instance of the SoftMax module
	softmaxModule.forward(input); // Perform the forward pass
	// Print the output tensor values
	Tensor output = softmaxModule.forward(input);
	printf("Output after SoftMax:\n");
	for (int i = 0; i < 32; i++) {
		printf("element %d: ", i);
		printf("%f ", output.getData()[i]);
		if ((i + 1) % 4 == 0) {
			printf("\n");
		}
	}
	return 0;
}

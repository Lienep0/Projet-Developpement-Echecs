#pragma once
#include "Tensor.h"

class Layer {
	private:
	Tensor weights;
	Tensor bias;
public:
	Layer(int input_size, int output_size) {
		int weights_dimension[] = {input_size, output_size};
		int bias_dimension[] = { output_size };
		this->weights = Tensor(weights_dimension);
		this->bias = Tensor(bias_dimension);
	}


	Layer() {
		this->weights = Tensor();
		this->bias = Tensor();
	}


	~Layer() {
		//The tensors will be automatically freed when the layer is destroyed
	}

	Tensor forward(Tensor input) {
		Tensor output = Tensor::multiply21(this->weights, input);
		output = Tensor::add(output, this->bias);
		return relu(output);
	}
};

#pragma once
#include "Tensor.cu"
#include <functional>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"



__global__ void multiply21h(Tensor a, Tensor b, Tensor result) {
	//Assuming it's 2d*1D (a*b)
	result.dev_data[threadIdx] = 0;
	for (int j = 0; j < a.dimensions[1]; j++) {
		result.dev_data[threadIdx] += a.dev_data[threadIdx * a.strides[0] + j * a.strides[1]] * b.dev_data[j * b.strides[0]];
	}
}



__global__ void addh(Tensor a, Tensor b, Tensor result) {
	//Assuming it's 1D+1D (a+b)
	

	result.dev_data[threadIdx] = a.dev_data[threadIdx * a.strides[0]] + b.dev_data[threadIdx * b.strides[0]];
		
}

class Layer {
	private:
	Tensor weights;
	Tensor bias;

	function<Tensor(Tensor)> activation = relu;
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
		return activation(output);
	}


	void forwardh(Tensor input, Tensor output) {
		//not the most efficient way of doing it but better in the our use case
		Tensor result(output.dimensions);
		multiply21h<<<1, this->weights.dimensions[1] >> > (this->weights, input, result);
		addh<<<1, this->bias.dimensions[0] >>> (result, this->bias, output);
	}

	void changeActivation(function<Tensor(Tensor)> newActivation) {
		this->activation = newActivation;
	}


};
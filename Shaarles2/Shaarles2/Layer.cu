#pragma once
#include "Tensor.cu"
#include <functional>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"


using namespace std;

__global__ void multiply21h(Tensor a, Tensor b, Tensor result) {
	//Assuming it's 2d*1D (a*b)
	printf("beginning to multiply 2D and 1D tensors in kernel with thread %d\n", threadIdx.x);
	result.dev_data[threadIdx.x] = 0;
	for (int j = 0; j < a.dimensions[1]; j++) {
		result.dev_data[threadIdx.x] += a.dev_data[threadIdx.x * a.strides[0] + j * a.strides[1]] * b.dev_data[j * b.strides[0]];
	}
	
}


__global__ void addh(Tensor a, Tensor b, Tensor result) {
	//Assuming it's 1D+1D (a+b)
	result.dev_data[threadIdx.x] = a.dev_data[threadIdx.x] + b.dev_data[threadIdx.x];
}

class Layer {
	private:
	Tensor weights;

	function<Tensor(Tensor)> activation = relu;
public:

	Tensor bias;
	Layer(int input_size, int output_size) {
		cout << "Initializing layer with input size " << input_size << " and output size " << output_size << endl;
		int weights_dimension[] = {output_size, input_size};
		int bias_dimension[] = { output_size };

		
		this->weights = Tensor(weights_dimension, 2);
		cout << "Initialized weights tensor :[" << weights.dimensions[0] << ", " << weights.dimensions[1] << "]" << endl;

		this->bias = Tensor(bias_dimension, 1);
	}


	Layer() {
		this->weights = Tensor();
		this->bias = Tensor(); 
	}


	~Layer() {
		//The tensors will be automatically freed when the layer is destroyed
	}

	Tensor forward(Tensor input) {
		Tensor output = Tensor::multiply21(weights, input);
		cout << "Input: " << endl;
		output = Tensor::add(output, bias);
		cout << "Output before activation: " << endl;
		return activation(output);
	}


	void forwardh(Tensor input, Tensor output) {
		//not the most efficient way of doing it but better in the our use case
		cout << output.dimensions[0] << " " << output.ndim << endl;
		Tensor result(output.dimensions, output.ndim);
		cout << "Launching kernel with " << this->weights.dimensions[0] << " threads" << endl;
		multiply21h<<<1, bias.dimensions[0] >> > (weights, input, result);
		cudaDeviceSynchronize();
		cout << "Finished multiplying, now adding bias" << endl;
		addh<<<1, bias.dimensions[0] >>> (result, this->bias, output);
		cudaDeviceSynchronize();
		output=activation(output);
	}

	void changeActivation(function<Tensor(Tensor)> newActivation) {
		this->activation = newActivation;
	}


};
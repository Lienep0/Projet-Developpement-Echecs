#pragma once
#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <cstdio>
#include <cstdlib>

using namespace std;



class Tensor {
	//2D and 3D tensors are the only ones we need for our network

public:
	int ndim;
	int* dimensions;
	int* strides = nullptr;//kinda like coordinates?
	float* data = nullptr;
	float* dev_data = nullptr; //for GPU tensors

	static bool canMultiply(Tensor a, Tensor b) {
		return a.dimensions[a.ndim - 1] == b.dimensions[0];
	}

	static Tensor multiply21(Tensor a, Tensor b) {
		//Assuming it's 2d*1D (a*b)
		
		Tensor result(b.dimensions);
		for(int i=0;i<a.dimensions[0];i++){
			result.data[i]=0;
			for(int j=0;j<a.dimensions[1];j++){
				result.data[i]+=a.data[i*a.strides[0]+j*a.strides[1]]*b.data[j*b.strides[0]];
			}
		}
		return result;

	}

	static Tensor add(Tensor a, Tensor b) {
		//Assuming it's 1D+1D (a+b)
		Tensor result(a.dimensions);
		for (int i = 0; i < a.dimensions[0]; i++) {
			result.data[i] = a.data[i * a.strides[0]] + b.data[i * b.strides[0]];
		}
		return result;
	}

	Tensor(int dimensions[]) {
		this->ndim = int(sizeof(dimensions) / sizeof(dimensions[0]));
		this->dimensions = dimensions;
		this->strides = new int[ndim];
		int nbEle = 1;
		for (int i = 0; i < ndim; i++) {
			this->strides[ndim - 1 - i] = nbEle;
			nbEle *= dimensions[i];
		}

		cudaMallocHost(&data, nbEle * sizeof(float));
		cudaMalloc(&dev_data, nbEle * sizeof(float));


	}
	Tensor(float dataT[]) {
		this->ndim = 1;
		this->dimensions = new int[1];
		this->dimensions[0] = (int)(sizeof(dataT) / sizeof(dataT[0]));
		this->strides = new int[ndim];
		int nbEle = 1;
		for (int i = 0; i < ndim; i++) {
			this->strides[ndim - 1 - i] = nbEle;
			nbEle *= dimensions[i];
		}

		cudaMallocHost(&data, nbEle * sizeof(float));
		cudaMalloc(&dev_data, nbEle * sizeof(float));

		for (int i = 0; i < nbEle; i++) {
			this->data[i] = dataT[i];
			this->dev_data[i] = dataT[i];
		}


	}

	Tensor() {
		this->ndim = 0;
		this->dimensions = nullptr;
		this->strides = nullptr;
		this->data = nullptr;
		this->dev_data = nullptr;
	}

	~Tensor() {
		cudaFreeHost(data);
		cudaFree(dev_data);
	}

	void toString() {
		printf("Tensor with %d dimensions\n", ndim);
		for (int i = 0; i < ndim; i++) {
			printf("Dimension %d: %d\n", i, dimensions[i]);
		}
	}

};

Tensor relu(Tensor input) {
	Tensor result(input.dimensions);
	for (int i = 0; i < input.dimensions[0]; i++) {
		result.data[i] = max(0.0f, input.data[i * input.strides[0]]);
	}
	return result;
}
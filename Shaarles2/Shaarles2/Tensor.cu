#pragma once
#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <random>

using namespace std;



class Tensor {
	//2D and 3D tensors are the only ones we need for our network

public:
	int ndim;
	int* dimensions;
	int* strides = nullptr;//kinda like coordinates?
	float* data = nullptr;
	float* dev_data = nullptr; //for GPU tensors


	Tensor(int dimensions[], int ndim) {

		cout << "Incoming dims: ";
		for (int i = 0; i < ndim; i++)
			cout << dimensions[i] << " ";
		cout << endl;


		this->ndim = ndim;
		this->dimensions = new int[ndim];
		for (int i = 0; i < ndim; i++) {
			this->dimensions[i] = dimensions[i];
		}
		this->strides = new int[ndim];
		int nbEle = 1;
		for (int i = 0; i < ndim; i++) {
			strides[ndim - 1 - i] = nbEle;
			cout << dimensions[i] << " nbEle: " << nbEle << endl;
			nbEle *= dimensions[i];
		}
		cout << "nbEle: " << nbEle << endl;


		cudaError_t err = cudaMallocHost(&data, nbEle * sizeof(float));
		if (err != cudaSuccess) {
			std::cerr << "cudaMallocHost failed: " << cudaGetErrorString(err) << std::endl;
			data = nullptr;
		}

		err = cudaMalloc(&dev_data, nbEle * sizeof(float));
		if (err != cudaSuccess) {
			std::cerr << "cudaMalloc failed: " << cudaGetErrorString(err) << std::endl;
			dev_data = nullptr;
		}

		for (int i = 0; i < nbEle; i++) {
			data[i] = static_cast<float>(rand()) / static_cast<float>(RAND_MAX);
		}
		cout << "Initialized tensor with random values" << endl;
	}


	Tensor(float* dataT, int size) {
		this->ndim = 1;
		this->dimensions = new int[1];
		this->dimensions[0] = size;
		this->strides = new int[ndim];
		int nbEle = 1;
		for (int i = 0; i < ndim; i++) {
			this->strides[ndim - 1 - i] = nbEle;
			cout << nbEle << endl;
			nbEle *= dimensions[i];
		}
		cout << "nbEle: " << nbEle << endl;

		cudaError_t err = cudaMallocHost(&data, nbEle * sizeof(float));
		if (err != cudaSuccess) {
			std::cerr << "On host cudaMallocHost failed: " << cudaGetErrorString(err) << std::endl;
			data = nullptr;
		}

		err = cudaMalloc(&dev_data, nbEle * sizeof(float));
		if (err != cudaSuccess) {
			std::cerr << "On host cudaMalloc failed: " << cudaGetErrorString(err) << std::endl;
			dev_data = nullptr;
		}


		cout << "Copying data to tensor" << endl;

		cudaMemcpy(data, dataT, nbEle * sizeof(float), cudaMemcpyHostToHost);
		cout << "Copied data to host memory" << endl;
		cudaMemcpy(dev_data, data, nbEle * sizeof(float), cudaMemcpyHostToDevice);
		cout << "Copied data to tensor" << endl;


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
	static bool canMultiply(Tensor a, Tensor b) {
		return a.dimensions[a.ndim - 1] == b.dimensions[0];
	}



	static Tensor add(float* a, float* b, int n) {
		//Assuming it's 1D+1D (a+b)
		float* resultData=nullptr;
		cudaError_t err = cudaMallocHost(&resultData, n * sizeof(float));
		if (err != cudaSuccess) {
			std::cerr << "cudaMallocHost failed: " << cudaGetErrorString(err) << std::endl;
			resultData = nullptr;
		}
		for (int i = 0; i < n; i++) {
			resultData[i] = a[i] + b[i];
		}
		Tensor result(resultData, n);
		cudaFreeHost(resultData);
		return result;
	}



	void toString() {
		printf("Tensor with %d dimensions\n", ndim);
		for (int i = 0; i < ndim; i++) {
			printf("Dimension %d: %d\n", i, dimensions[i]);
		}
	}

};



Tensor multiply21(Tensor a, Tensor b) {
	//Assuming it's 2d*1D (a*b)
	cout << "b.dimensions[0]: " << b.dimensions[0] << " ndim: " << b.ndim << endl;
	Tensor result(b.dimensions, b.ndim);
	cout << "Multiplying 2D and 1D tensors " << endl;
	for (int i = 0; i < b.dimensions[0]; i++) {
		cout << "Calculating result.data[" << i << "]" << endl;
		result.data[i] = 0;
		cout << "result.data[" << i << "] = 0.0f" << endl;
		for (int j = 0; j < a.dimensions[1]; j++) {
			result.data[i] += a.data[i * a.strides[0] + j * a.strides[1]] * b.data[j * b.strides[0]];
			cout << "result.data[" << i << "] += a.data[" << i * a.strides[0] + j * a.strides[1] << "] * b.data[" << j * b.strides[0] << "]" << endl;
		}
	}
	return result;

}


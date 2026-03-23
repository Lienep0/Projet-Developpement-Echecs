#pragma once
#include <cstdio>
#include <cstdlib>
#include "Layer.h"
using namespace std;

class Network {
private:
	int* dimensions;
	Tensor weights;
	int w_length = 1;
	int* w_dimensions;
	Tensor biases;
	int b_length = 1;
	int* b_dimensions;
	int size;

	//useful device properties
	int maxSharedMemPerBlock;
	int maxNbThreadsPerBlock;
public:

	Network(int dimensions[], int maxSharedMemPerBlock, int maxNbThreadsPerBlock) {
		this->maxSharedMemPerBlock = maxSharedMemPerBlock;
		this->maxNbThreadsPerBlock = maxNbThreadsPerBlock;
		this->dimensions = dimensions;
		this->size = sizeof(dimensions) / sizeof(dimensions[0]);
		b_dimensions = new int[size - 1];
		w_dimensions = new int[size - 1];
		for (int i = 1; i < size; i++) {
			w_dimensions[i - 1] = dimensions[i - 1] * dimensions[i];
			b_dimensions[i - 1] = dimensions[i];
		}
		for (int i = 0; i < size - 1; i++) {
			b_length *= b_dimensions[i];

			w_length *= w_dimensions[i];
		}
		weights = Tensor(w_length, w_dimensions);
		biases = Tensor(b_length, b_dimensions);


	}

	~Network() {
	}
	void toString();



};

void Network::toString() {
	printf("Network with %d layers\n", size);
	for (int i = 0; i < size - 1; i++) {
		printf("Layer %d: %d neurons\n", i, dimensions[i]);
	}
}
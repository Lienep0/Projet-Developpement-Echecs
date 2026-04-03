#pragma once
#include "Layer.cu"
#include <cstring>
#include <iostream>


class Network
{
private:
	int* dimensions;
	Layer* layers;
	int nbLayers;

public:
	Network(int dimensions[],int ndim) {
		this->dimensions = dimensions;
		this->nbLayers = ndim-1;
		cout << nbLayers << endl;
		this->layers = new Layer[nbLayers];
		for (int i = 0; i < nbLayers; i++) {
			this->layers[i] = Layer(dimensions[i], dimensions[i + 1]);
		}
	}

	void forward(float entry[], int size) {
		Tensor entryTensor(entry, size);
		for (int i = 0; i < nbLayers; i++) {
			entryTensor = layers[i].forward(entryTensor);
		}

	}
	void forwardh(float entry[], int size) {
		//should be sufficiently debuged
		cout << "Starting forwardh with entry size: " << size << endl;
		Tensor entryTensor(entry, size);
		cout << "Initialized entry tensor with dimensions: [" << entryTensor.dimensions[0] << "] and data: " << entryTensor.data[0] << endl;
		cout << "starting to forward the data through the layers, we will use the same tensor for input and output to save memory" << endl;

		Tensor outputTensor(layers[0].bias.dimensions, layers[0].bias.ndim);
		layers[0].forwardh(entryTensor, outputTensor);
		entryTensor = outputTensor;

		for (int i = 1; i < nbLayers; i++) {
			cout << "new output tensor with dimensions: [" << layers[i].bias.dimensions[0] << "] and data: " << layers[i].bias.data[0] << endl;
			outputTensor = Tensor(layers[i].bias.dimensions, layers[i].bias.ndim);
			cout << "Forwarding through layer " << i << " with input dimensions: [" << entryTensor.dimensions[0] << "] and output dimensions: [" << outputTensor.dimensions[0] << "]" << endl;
			layers[i].forwardh(entryTensor, outputTensor);
			entryTensor = outputTensor;
		}

	}

	
};
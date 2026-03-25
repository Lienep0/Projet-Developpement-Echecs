#pragma once
#include "Layer.h"


class Network
{
private:
	int* dimensions;
	Layer* layers;
	int nbLayers;

public:
	Network(int* dimensions) {
		this->dimensions = dimensions;
		this->nbLayers = sizeof(dimensions)/sizeof(dimensions[0]);
		this->layers = new Layer[nbLayers];
		for (int i = 0; i < nbLayers; i++) {
			this->layers[i] = Layer(dimensions[i], dimensions[i + 1]);
		}
	}

	void forward(float entry[]) {
		Tensor entryTensor(entry);
		for(int i = 0; i < nbLayers; i++) {
			entryTensor=this->layers[i].forward(entryTensor);
		}
		
	}

};

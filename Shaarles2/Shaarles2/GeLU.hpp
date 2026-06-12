#pragma once
#include <cstdio>
#include "Tensor.cu"
#include <cstdlib>
#include "Module.cu"

using namespace std;

__global__ void tanh(float* input, float* output, int n);

__global__ void sqrt(float* input, float* output, int n);

__global__ void gelu(float* input, float* output, int n);

class GeLU : public Module {
private:
	Tensor input;

public:

	Tensor forward(Tensor input) override;

	void backward(Tensor input, Tensor gradOutput) override;
};

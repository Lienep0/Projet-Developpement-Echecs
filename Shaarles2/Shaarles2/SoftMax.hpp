#pragma once
#include <cstdio>
#include <cstdlib>
#include "Module.cu"

using namespace std;

__global__ void max_search(int num_features, float* input_data, float* output_data, int B, int lasts);

__global__ void t_to_t_substraction(float* input_data, float* max_data, int B, int C, int lasts);
__global__ void exp_and_sum(float* input_data, float* sum_data, int B, int C, int lasts);
__global__ void div_by_sum(float* input_data, float* sum_data, int B, int C, int lasts);


class SoftMax : public Module {
private:
	Tensor weights;
	bool training;
	Tensor maxc;
	int dim; //not sure I understand what this "dimension of normalization" is.
	Tensor sumc;


public:
	SoftMax(int dim);
	Tensor forward(Tensor input);
		//input is of shape (B, num_features, lasts)
		//output is of shape (B, num_features, lasts)

};


#pragma once
#include <cstdio>
#include "Tensor.cu"
#include <cstdlib>
#include "Module.cu"

using namespace std;

__global__ void max_search(int num_features, float* input_data, float* output_data, int B, int lasts);

__global__ void t_to_t_substraction(float* input_data, float* max_data, int size);
__global__ void exp_and_sum(float* input_data, float* sum_data, int size);
__global__ void div_by_sum(float* input_data, float* sum_data, int size);


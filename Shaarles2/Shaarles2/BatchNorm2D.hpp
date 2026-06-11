#pragma once

#include <cstdio>
#include <cstdlib>
#include "Module.cu"

using namespace std;

//implementation of reduced batch mean, so we can use a bit of paralelization to speed up the process

__global__ void batch_mean_reduced(int num_features, float* input_data, float* batch_mean_data, int m, int B, int lasts);


//implementation of reduced batch variance, so we can use a bit of paralelization to speed up the process
__global__ void batch_var_reduced(int num_features, float* input_data, float* batch_var_data, float* batch_mean_data, int m, int B, int lasts);

__global__ void normalization(int num_features, float* input_data, float* output_data, float* batch_mean_data,
	float* batch_var_data, float* weights_data, float* bias_data, int B, int lasts);


//updating the running mean
__global__ void update_running_mean(int num_features, float* running_mean_data, float* batch_mean_data, float momentum);
//updating the running variance
__global__ void update_running_var(int num_features, float* running_var_data, float* batch_var_data, float momentum);

class BatchNorm2D : public Module {

private:
	//used only in inference
	Tensor running_mean;
	Tensor running_var;

	//used both in inference and training
	Tensor gamma;
	Tensor beta;


	//used only in training
	Tensor batch_mean;
	Tensor batch_var;

	int num_features;
public:


	BatchNorm2D(int num_features);

	Tensor forward(Tensor input) override;
		/*
		Implementing the forward pass for batch normalization


		input are assumed to be in the format(B, C, H, W, ...)
		but for Loukka's network input are assumed to be in the format(B, C, H, W)
			B -> the batch index
			C -> the channel index
			H -> the height index
			W -> the width index
			but just in case I'm going to make it work for any number of dimensions

		*/

	// Implement the backward pass 	
	void backward(Tensor input, Tensor gradOutput) override;

	bool is_training() const;
	void set_training(bool t);

};
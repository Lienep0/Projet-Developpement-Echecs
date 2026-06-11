#include <cstdio>
#include "Tensor.cu"
#include <cstdlib>
#include "Module.cu"

using namespace std;


//implementation of a kind of reduced max, not the most efficient
// and I think it should be done closely to what was done for batchNorm2d(I might be wrong)
//but let's hope not

__global__ void max_search(int num_features, float* input_data, float* output_data, float* batch_mean_data, float* batch_var_data, float* weights_data, float* bias_data, int B, int lasts) {
	int coordinate = blockIdx.x * blockDim.x + threadIdx.x;
	float max_value = -FLT_MAX;
	if (coordinate >= num_features) return;
	for (int i = 0; i < B; i++) {
		for (int ic = 0; ic < lasts; ic++) {
			int idx = i * num_features * lasts + coordinate * lasts + ic;
			//arbitrarily small epsilon (=1e-5f) value to prevent division by zero
			if (max_value < input_data[idx]) {
				max_value = input_data[idx];
			}
		}
	}
	output_data[coordinate] = max_value;
}

__global__ void t_to_t_substraction(float* input_data, float* max_data, int size) {
	int idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx >= size) return;
	input_data[idx] = input_data[idx] - max_data[idx % (size / (gridDim.x * blockDim.x))];

}

__global__ void exp_and_sum(float* input_data, float* sum_data, int size) {
	int idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx >= size) return;
	input_data[idx] = expf(input_data[idx]);
	atomicAdd(&sum_data[idx % (size / (gridDim.x * blockDim.x))], input_data[idx]);
}

__global__ void div_by_sum(float* input_data, float* sum_data, int size) {
	int idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx >= size) return;
	input_data[idx] = input_data[idx] / sum_data[idx % (size / (gridDim.x * blockDim.x))];
}

class SoftMax : public Module {
private:
	Tensor weights;
	bool training;
	Tensor maxc;
	int dim; //not sure I understand what this "dimension of normalization" is.
	
public:
	SoftMax(int dim) : dim(dim){
		training = true;

	}
	Tensor forward(Tensor input) {
		//input is of shape (B, num_features, lasts)
		//output is of shape (B, num_features, lasts)
		Tensor output(input.dimensions, input.ndim);
		maxc = Tensor(&input.dimensions[1], 1);
		int threadsPerBlock = 256;
		int blocksPerGrid = (input.dimensions[1] + threadsPerBlock - 1) / threadsPerBlock;
		max_search << <blocksPerGrid, threadsPerBlock >> > (input.dimensions[1], input.dev_data, maxc.dev_data, nullptr, nullptr, nullptr, nullptr, input.dimensions[0], input.dimensions[2]);
		cudaDeviceSynchronize();

		//synchronization so the values are on both dev and host before the next kernel
		maxc.sync_data("dev_data", "data", maxc.dimensions[0] * sizeof(float));

		int total_size = input.dimensions[0] * input.dimensions[1] * input.dimensions[2];
		threadsPerBlock = 256;
		blocksPerGrid = (total_size + threadsPerBlock - 1) / threadsPerBlock;


		return output;
	}

};

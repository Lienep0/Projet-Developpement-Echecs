#include <cstdio>
#include <cstdlib>
#include "Module.cu"


//implementation of reduced batch mean, so we can use a bit of paralelization to speed up the process

__global__ void batch_mean_reduced(int num_features, float* input_data, float* batch_mean_data, int m, int B, int lasts) {
	int coordinate = blockIdx.x * blockDim.x + threadIdx.x;
	if (coordinate >= num_features) return;

	float sum = 0.0f;

	for (int i = 0; i < B; i++) {
		for (int ic = 0; ic < lasts; ic++) {
			sum += input_data[i * num_features * lasts + coordinate * lasts + ic];
		}
	}
	batch_mean_data[coordinate] = sum / m;
}


//implementation of reduced batch variance, so we can use a bit of paralelization to speed up the process
__global__ void batch_var_reduced(int num_features, float* input_data, float* batch_var_data, float* batch_mean_data, int m, int B, int lasts) {
	int coordinate = blockIdx.x * blockDim.x + threadIdx.x;
	if (coordinate >= num_features) return;

	float sum = 0.0f;
	float diff;

	for (int i = 0; i < B; i++) {
		for (int ic = 0; ic < lasts; ic++) {
			diff = input_data[i * num_features * lasts + coordinate * lasts + ic] - batch_mean_data[coordinate];
			sum += diff * diff;
		}
	}
	batch_var_data[coordinate] = sum / m;
}

__global__ void normalization(int num_features, float* input_data, float* output_data, float* batch_mean_data, float* batch_var_data, float* weights_data, float* bias_data, int B, int lasts) {
	int coordinate = blockIdx.x * blockDim.x + threadIdx.x;
	if (coordinate >= num_features) return;
	for (int i = 0; i < B; i++) {
		for (int ic = 0; ic < lasts; ic++) {
			int idx = i * num_features * lasts + coordinate * lasts + ic;
			//arbitrarily small epsilon (=1e-5f) value to prevent division by zero
			output_data[idx] = (input_data[idx] - batch_mean_data[coordinate]) / sqrtf(batch_var_data[coordinate] + 1e-5f) * weights_data[coordinate] + bias_data[coordinate];
		}
	}
}


//updating the running mean
__global__ void update_running_mean(int num_features, float* running_mean_data, float* batch_mean_data, float momentum) {
	int coordinate = blockIdx.x * blockDim.x + threadIdx.x;
	if (coordinate >= num_features) return;

	running_mean_data[coordinate] = (1.0f - momentum) * running_mean_data[coordinate] + momentum * batch_mean_data[coordinate];
}

//updating the running variance
__global__ void update_running_var(int num_features, float* running_var_data, float* batch_var_data, float momentum) {
	int coordinate = blockIdx.x * blockDim.x + threadIdx.x;
	if (coordinate >= num_features) return;

	running_var_data[coordinate] = (1.0f - momentum) * running_var_data[coordinate] + momentum * batch_var_data[coordinate];
}

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


	BatchNorm2D(int num_features) {
		// Initialize weights and bias
		//while less compact I'm going back to this older initalization method to not add another Tensor constructor xd

		this->num_features = num_features;

		running_mean = Tensor(new float[num_features](), num_features);
		running_var = Tensor(new float[num_features](), num_features);

		gamma = Tensor(new float[num_features](), num_features);
		gamma.one();

		beta = Tensor(new float[num_features](), num_features);
		beta.zero();

		batch_mean = Tensor(new float[num_features](), num_features);
		batch_var = Tensor(new float[num_features](), num_features);

	}
	Tensor forward(Tensor input) override {
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

		int ndim = input.ndim;

		int B = input.dimensions[0];
		int C = input.dimensions[1];

		if (C != num_features) {
			std::cerr << "Error: BatchNorm2D num_features != input channels" << std::endl;
			exit(1);
		}


		//number of elements in each channel
		int m = B;


		for (int i = 2; i < ndim; i++) {
			m *= input.dimensions[i];
		}

		int lasts = m / B;

		//compute necessary sizes for the kernels' launch
		int bloc_size = 256;
		int grid_size = (num_features + bloc_size - 1) / bloc_size;

		Tensor output(input.dimensions, input.ndim); // Create an output tensor with the same dimensions as input
		if (training) {
			//Computing batch mean 
			batch_mean_reduced << <grid_size, bloc_size >> > (num_features, input.dev_data, batch_mean.dev_data, m, B, lasts);
			cudaDeviceSynchronize();

			cudaError_t cuderr = cudaMemcpy(batch_mean.data, batch_mean.dev_data, num_features * sizeof(float), cudaMemcpyDeviceToHost);
			if (cuderr != cudaSuccess) {
				std::cerr << "On host cudaMemcpy failed: " << cudaGetErrorString(cuderr) << std::endl;

			}


			//computing batch var
			batch_var_reduced << <grid_size, bloc_size >> > (num_features, input.dev_data, batch_var.dev_data, m, B, lasts);
			cudaDeviceSynchronize();

			cuderr = cudaMemcpy(batch_var.data, batch_var.dev_data, num_features * sizeof(float), cudaMemcpyDeviceToHost);
			if (cuderr != cudaSuccess) {
				std::cerr << "On host cudaMemcpy failed: " << cudaGetErrorString(cuderr) << std::endl;

			}


			//now normalizing the input using the batch mean and variance
			normalization << <grid_size, bloc_size >> > (num_features, input.dev_data, output.dev_data, batch_mean.dev_data, batch_var.dev_data, gamma.dev_data, beta.dev_data, B, lasts);
			cudaDeviceSynchronize();

			cuderr = cudaMemcpy(output.data, output.dev_data, m * C * sizeof(float), cudaMemcpyDeviceToHost);
			if (cuderr != cudaSuccess) {
				std::cerr << "On host cudaMemcpy failed: " << cudaGetErrorString(cuderr) << std::endl;

			}

			//Update of running mean and running variance

			update_running_mean << <grid_size, bloc_size >> > (num_features, running_mean.dev_data, batch_mean.dev_data, 0.1f);
			cudaDeviceSynchronize();

			cuderr = cudaMemcpy(running_mean.data, running_mean.dev_data, num_features * sizeof(float), cudaMemcpyDeviceToHost);
			if (cuderr != cudaSuccess) {
				std::cerr << "On host cudaMemcpy failed: " << cudaGetErrorString(cuderr) << std::endl;
			}

			update_running_var << <grid_size, bloc_size >> > (num_features, running_var.dev_data, batch_var.dev_data, 0.1f);
			cudaDeviceSynchronize();

			cuderr = cudaMemcpy(running_var.data, running_var.dev_data, num_features * sizeof(float), cudaMemcpyDeviceToHost);
			if (cuderr != cudaSuccess) {
				std::cerr << "On host cudaMemcpy failed: " << cudaGetErrorString(cuderr) << std::endl;
			}
		}
		else {
			// Use running mean and variance for normalization during inference

			normalization << <grid_size, bloc_size >> > (num_features, input.dev_data, output.dev_data, running_mean.dev_data, running_var.dev_data, gamma.dev_data, beta.dev_data, B, lasts);
			cudaDeviceSynchronize();

			cudaError_t cuderr = cudaMemcpy(output.data, output.dev_data, m * C * sizeof(float), cudaMemcpyDeviceToHost);
			if (cuderr != cudaSuccess) {
				std::cerr << "On host cudaMemcpy failed: " << cudaGetErrorString(cuderr) << std::endl;
			}
		}
		return output;
	}

	void backward(Tensor input, Tensor gradOutput) override {
		// Implement the backward pass to compute gradients for weights and bias
	}

	bool is_training() const { return training; }
	void set_training(bool t) { training = t; }

};
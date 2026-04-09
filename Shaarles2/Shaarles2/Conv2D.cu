#include <cstdio>
#include "Module.cu"
#include <cstdlib>

class Conv2D : public Module {
private:
	int in_channels;
	int out_channels;
	int* kernel_size;
	Tensor weights;
	Tensor bias;
public:
	Conv2D(int in_channels, int out_channels, int* kernel_size) :
		in_channels(in_channels), out_channels(out_channels), kernel_size(kernel_size),
		weights(new int[4] {out_channels, in_channels, kernel_size[0], kernel_size[1]}, 4),
		bias(new int[1] {out_channels}, 1) {
	
	}

	void forward(Tensor& input, Tensor& output) override{
		
	}
};
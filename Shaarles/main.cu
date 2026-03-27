#include "Network.cu"
#include <chrono>
#include <iostream>


using namespace std;

int main() {
	int dimensions[] = {784, 128, 64, 250,10};
	Network network(dimensions);

	//test forward and time it

	chrono::steady_clock::time_point start = chrono::steady_clock::now();
	network.forward(new float[784]);
	chrono::steady_clock::time_point end = chrono::steady_clock::now();
	cout << "Forward pass took " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << " milliseconds" << endl;

	//test on device

	start = chrono::steady_clock::now();
	network.forwardh(new float[784]);
	end = chrono::steady_clock::now();
	cout << "Forward pass on device took " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << " milliseconds" << endl;


	return 0;
}
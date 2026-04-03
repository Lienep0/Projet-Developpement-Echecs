#include <cstdio>
#include <cstdlib>
#include "Network.cu"
#include <chrono>
#include <iostream>

using namespace std;

int main() {
	int dimensions[] = {5,16,16,10};	
	Network network(dimensions, sizeof(dimensions) / sizeof(dimensions[0]));

	float entry[] = { 1,2,3,4,5 };
	int size = sizeof(entry) / sizeof(entry[0]);
	cout << "network initalized"<< endl;


	//measuring in the case of cpu usage
	chrono::system_clock::time_point start = chrono::system_clock::now();
	network.forward(entry, size);
	chrono::system_clock::time_point end = chrono::system_clock::now();

	cout << "Time taken: " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << "ms" << endl;


	
	//measuring in the case of gpu usage
	start = chrono::system_clock::now();

	cout << "forwarding" << endl;
	network.forwardh(entry, size);

	cout << "forwarded" << endl;
	end = chrono::system_clock::now();

	cout << "Time taken: " << chrono::duration_cast<chrono::milliseconds>(end - start).count() << "ms" << endl;


	
	return 0;
}
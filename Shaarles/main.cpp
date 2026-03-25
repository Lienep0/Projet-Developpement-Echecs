#include "Network.h"

using namespace std;

int main() {
	int dimensions[] = {784, 128, 64, 10};
	Network network(dimensions);
	network.forward(new float[784]);
	return 0;
}
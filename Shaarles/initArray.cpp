#include "initArray.h"


void initArray(float* arr, int length) {
	for (int i = 0; i < length; i++) {
		arr[i] = 1.0f;
	}
}
//overloaded function for int array
void initArray(int* arr, int length) {
	for (int i = 0; i < length; i++) {
		arr[i] = 1.0f;
	}
}

void printArray(int* arr, int length) {
	for (int i = 0; i < length; i++) {
		cout << arr[i] << endl;
	}
}

//overloaded function for float array
void printArray(float* arr, int length) {
	for (int i = 0; i < length; i++) {
		cout << arr[i] << endl;
	}
}
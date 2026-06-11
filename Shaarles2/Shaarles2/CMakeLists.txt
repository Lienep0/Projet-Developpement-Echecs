cmake_minimum_required(VERSION 3.18)
project(ShAIrles LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 17)

find_package(Python REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

pybind11_add_module(ShAIrles
    bindings.cpp
    Tensor.cu
    Conv2D.cu
    Linear.cu
    GeLU.cu
    SoftMax.cu
    BatchNorm2D.cu
)

set_target_properties(ShAIrles PROPERTIES CUDA_SEPARABLE_COMPILATION ON)

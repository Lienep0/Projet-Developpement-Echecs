cmake_minimum_required(VERSION 3.26)
project(ShAIrles LANGUAGES CXX CUDA)

# Finding Python + pybind11
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 REQUIRED)

# Activating CUDA
enable_language(CUDA)

# Source files
set(SOURCES
    bindings.cu
    Tensor.cu
    Module.cu
    Conv2D.cu
    BatchNorm2D.cu
    GeLU.cu
    SoftMax.cu
    Linear.cu
)

# Creating the Python Module
pybind11_add_module(ShAIrles MODULE ${SOURCES})

# Flags CUDA
set_target_properties(ShAIrles PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
    CUDA_ARCHITECTURES "native"

    

)

target_link_libraries(ShAIrles PRIVATE cudart)

link_directories("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.2/lib/x64")


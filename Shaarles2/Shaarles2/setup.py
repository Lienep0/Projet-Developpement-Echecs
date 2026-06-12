from setuptools import setup
from setuptools_cuda_cpp import CUDAExtension, BuildExtension
import pybind11
import os

sources = [
    "bindings.cu",        # compilé par NVCC uniquement
]

setup(
    name="ShAIrles",
    version="0.1.0",
    description="Mini deep learning library (C++/CUDA)",
    ext_modules=[
        CUDAExtension(
            name="ShAIrles",
            sources=sources,
            include_dirs=[
                ".",                                # ton projet
                pybind11.get_include(),             # pybind11
                pybind11.get_include(user=True),    # pybind11 (user)
            ],
            extra_compile_args={
                "cxx": [
                    "/O2",
                    "/EHsc",
                    "/std:c++17",
                ],
                "nvcc": [
                    "-O3",
                    "--use_fast_math",
                    "-std=c++17",
                    "-Xcompiler", "/MD",
                    "-Xcompiler", "/EHsc",
                    "-arch=sm_75",   # adapte selon ta carte
                ],
            },
            libraries=["cudart"],
        )
    ],
    cmdclass={"build_ext": BuildExtension},
)

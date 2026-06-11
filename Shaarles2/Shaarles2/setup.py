from setuptools_cuda_cpp import CUDAExtension, BuildExtension
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
import pybind11

ext_modules = [
    CUDAExtension(  # Utilise CUDAExtension au lieu de Pybind11Extension
        "ShAIrles",
        [
            "bindings.cpp",
            "BatchNorm2D.cu",
            "Conv2D.cu",
            "Tensor.cu",
            "Module.cu",
            "Linear.cu",
            "SoftMax.cu"
        ],
        include_dirs=[
            pybind11.get_include(),
            pybind11.get_include(user=True),
            "."
        ],
        extra_compile_args={
            "cxx": ["-O3", "-std=c++17"],
            "nvcc": [
                "-O3",
                "-std=c++17",
                "--expt-relaxed-constexpr",
                "-Xcompiler", "-fPIC"
            ]
        },
        libraries=["cudart"],
    )
]

setup(
    name="ShAIrles",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExtension}, # Utilise BuildExtension
)
from distutils.ccompiler import new_compiler
from distutils.sysconfig import customize_compiler

# Add .cu to the list of known file types
import distutils.ccompiler
distutils.ccompiler.CCompiler.src_extensions.append('.cu')
distutils.ccompiler.CCompiler.object_extensions.append('.cu')

from setuptools import setup
from setuptools.command.build_ext import build_ext
from pybind11.setup_helpers import Pybind11Extension
import sys
import os

class BuildExt(build_ext):
    def build_extensions(self):
        ct = self.compiler.compiler_type
        for ext in self.extensions:
            if ct == "msvc":
                # Flags MSVCj on Windows
                ext.extra_compile_args = {
                    "cxx": ["/O2", "/EHsc"],
                    "nvcc": [
                        "-O3",
                        "-std=c++17",
                        "--expt-relaxed-constexpr",
                        "-Xcompiler=/EHsc",
                    ]
                }
            else:
                # Linux
                ext.extra_compile_args = {
                    "cxx": ["-O3", "-std=c++17", "-fPIC"],
                    "nvcc": [
                        "-O3",
                        "-std=c++17",
                        "--expt-relaxed-constexpr",
                        "-Xcompiler=-fPIC",
                    ]
                }
        build_ext.build_extensions(self)

ext_modules = [
    Pybind11Extension(
        "ShAIrles",
        [
            "bindings.cpp",
            "Tensor.cu",
            "Conv2D.cu",
            "BatchNorm2D.cu",
            "Linear.cu",
            "GeLU.cu",
            "ReLU.cu",
            "SoftMax.cu",
        ],
        include_dirs=["."],
        libraries=["cudart"],
    )
]

setup(
    name="ShAIrles",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExt},
)

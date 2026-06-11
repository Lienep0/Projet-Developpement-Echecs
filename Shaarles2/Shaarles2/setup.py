from setuptools import setup
from setuptools.command.build_ext import build_ext
from pybind11.setup_helpers import Pybind11Extension
import sys
import setuptools

class BuildExt(build_ext):
    def build_extensions(self):
        ct = self.compiler.compiler_type
        for ext in self.extensions:
            if hasattr(ext, "extra_compile_args"):
                if ct == "unix":
                    ext.extra_compile_args = ext.extra_compile_args.get("cxx", [])
                else:
                    ext.extra_compile_args = []
        build_ext.build_extensions(self)

ext_modules = [
    Pybind11Extension(
        "ShAIrles",
        [
            "bindings.cpp",
            "BatchNorm2D.cu",
            "Conv2D.cu",
            "Tensor.cpp",
            "Module.cpp",
        ],
        include_dirs=["."],
        extra_compile_args={
            "cxx": ["-O3", "-std=c++17"],
            "nvcc": ["-O3", "-std=c++17", "--expt-relaxed-constexpr"]
        },
        libraries=["cudart"],
    )
]

setup(
    name="ShAIrles",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExt},
)

from setuptools import setup
from setuptools.command.build_ext import build_ext
from distutils.sysconfig import get_config_vars
from pybind11.setup_helpers import Pybind11Extension
import sys
import os

# Remove -Wstrict-prototypes (Python bug)
(opt,) = get_config_vars("OPT")
os.environ["OPT"] = " ".join(flag for flag in opt.split() if flag != "-Wstrict-prototypes")

class BuildExt(build_ext):
    def build_extensions(self):
        # Force NVCC for .cu files
        for ext in self.extensions:
            for i, src in enumerate(ext.sources):
                if src.endswith(".cu"):
                    ext.sources[i] = src  # keep name
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
    cmdclass={"build_ext": BuildExt},
)

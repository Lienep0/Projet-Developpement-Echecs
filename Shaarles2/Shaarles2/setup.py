from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [ Pybind11Extension("ShAIrles", ["Conv2d.cu", "Tensor.cu", "GeLU.cu", "SoftMax.cu", "BatchNorm2D.cu", "Module.cu", "Linear.cu"], include_dirs=["."], extra_compile_args={ "nvcc": ["-O3", "-std=c++17", "--expt-relaxed-constexpr"] },libraries=["cudart"], library_dirs=[], runtime_library_dirs=[],)]

setup(
    name="mycuda",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
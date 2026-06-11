from setuptools_cuda_cpp import CUDAExtension, BuildExtension

ext_modules = [
    CUDAExtension(  # Utilise CUDAExtension au lieu de Pybind11Extension
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
    cmdclass={"build_ext": BuildExtension}, # Utilise BuildExtension
)
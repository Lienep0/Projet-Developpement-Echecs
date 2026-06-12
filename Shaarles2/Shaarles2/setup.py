import os
import sys
import setuptools
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

class CUDA_build_ext(build_ext):
    def build_extensions(self):
        # Register .cu extension
        self.compiler.src_extensions.append('.cu')
        self.compiler.set_executable('compiler_so', 'nvcc')
        self.compiler.set_executable('linker_so', 'nvcc --shared')
        
        if sys.platform == 'win32':
            for ext in self.extensions:
                # Ensure extra_compile_args exists
                if not hasattr(ext, 'extra_compile_args'):
                    ext.extra_compile_args = {}
                
                # If it's a dict (common when passed as {'nvcc': [...]}), update the 'nvcc' key
                if isinstance(ext.extra_compile_args, dict):
                    nvcc_args = ext.extra_compile_args.get('nvcc', [])
                    
                    # Check if flag already exists to avoid duplicates
                    if not any('/Zc:preprocessor' in arg for arg in nvcc_args):
                        nvcc_args.append('-Xcompiler=/Zc:preprocessor')
                    
                    ext.extra_compile_args['nvcc'] = nvcc_args
                    
                    # Also ensure host compiler (MSVC) gets the flag if compiling C++ wrappers
                    cxx_args = ext.extra_compile_args.get('cxx', [])
                    if not any('/Zc:preprocessor' in arg for arg in cxx_args):
                        cxx_args.append('/Zc:preprocessor')
                    ext.extra_compile_args['cxx'] = cxx_args

                # If it's a list (legacy flat list), append directly
                elif isinstance(ext.extra_compile_args, list):
                    if '-Xcompiler=/Zc:preprocessor' not in ext.extra_compile_args:
                        ext.extra_compile_args.append('-Xcompiler=/Zc:preprocessor')

        build_ext.build_extensions(self)

# Define your extension
# NOTE: extra_compile_args is passed as a DICT here
cuda_ext = Extension(
    name='ShAIrles',
    sources=['bindings.cpp', 'Tensor.cu', 'Conv2D.cu', 'Linear.cu', 'GeLU.cu', 'SoftMax.cu', 'BatchNorm2D.cu', 'ReLU.cu', 'Module.cu'], # Add your .cpp files here if any
    extra_compile_args={
        'nvcc': [
            '-O3',
            '--ptxas-options=-v',
            # We will inject /Zc:preprocessor via build_extensions, 
            # but adding it here is safe too.
            '-Xcompiler=/Zc:preprocessor' 
        ],
        'cxx': [
            '/Zc:preprocessor',
            '/O2'
        ]
    },
    library_dirs=[os.environ.get('CUDA_PATH', '') + '\\lib\\x64'],
    libraries=['cudart']
)

setup(
    name='ShAIrles',
    version='0.1',
    ext_modules=[cuda_ext],
    cmdclass={'build_ext': CUDA_build_ext},
    zip_safe=False,
)
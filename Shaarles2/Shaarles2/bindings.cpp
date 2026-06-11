#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Tensor.hpp"
#include "Conv2D.hpp"
#include "BatchNorm2D.hpp"
#include "Module.hpp"

namespace py = pybind11;

// Si tu utilises des pointeurs CUDA depuis Python (PyTorch)
template<typename T>
T* ptr_from_uintptr(uintptr_t p) {
    return reinterpret_cast<T*>(p);
}

PYBIND11_MODULE(ShAIrles, m) {
    m.doc() = "C++/CUDA deep learning engine by Charles";

    // -------------------------
    //  Tensor
    // -------------------------
    py::class_<Tensor>(m, "Tensor")
        .def(py::init<const std::vector<int>&>())   // Tensor([1,3,32,32])
        .def("to_cuda", &Tensor::to_cuda)
        .def("to_cpu", &Tensor::to_cpu)
        .def("numel", &Tensor::numel)
        .def("shape", &Tensor::shape)
        .def_readwrite("data", &Tensor::data)       // CPU pointer
        .def_readwrite("dev_data", &Tensor::dev_data); // CUDA pointer

    // -------------------------
    //  Conv2D
    // -------------------------
    py::class_<Conv2D>(m, "Conv2D")
        .def(py::init<int, int, int, int, int>(),
            py::arg("in_channels"),
            py::arg("out_channels"),
            py::arg("kernel_size"),
            py::arg("stride") = 1,
            py::arg("padding") = 0)
        .def("forward", &Conv2D::forward)
        .def("forward_ptr", [](Conv2D& self, uintptr_t x_ptr, uintptr_t out_ptr,
            int H, int W) {
                float* x = ptr_from_uintptr<float>(x_ptr);
                float* out = ptr_from_uintptr<float>(out_ptr);
                self.forward_ptr(x, out, H, W);
            })
        .def_readwrite("weights", &Conv2D::weights)
        .def_readwrite("bias", &Conv2D::bias);

#include "Tensor.cu"
#include "Conv2D.cu"
#include "BatchNorm2D.cu"
#include "Module.cu"
#include "SoftMax.cu"
#include "Linear.cu"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(ShAIrles, m) {
    m.doc() = "C++/CUDA deep learning engine by Charles";

    // -------------------------
    // Tensor
    // -------------------------
    py::class_<Tensor>(m, "Tensor")
        .def(py::init<const std::vector<int>&>())
        .def("to_cuda", &Tensor::to_cuda)
        .def("to_cpu", &Tensor::to_cpu)
        .def("numel", &Tensor::numel)
        .def("shape", &Tensor::shape)
        .def_readwrite("data", &Tensor::data)
        .def_readwrite("dev_data", &Tensor::dev_data);

    // -------------------------
    // Conv2D
    // -------------------------
    py::class_<Conv2D>(m, "Conv2D")
        .def(py::init<int, int, int, int, int>())
        .def("forward", &Conv2D::forward)
        .def_readwrite("weights", &Conv2D::weights)
        .def_readwrite("bias", &Conv2D::bias);

    // -------------------------
    // BatchNorm2D
    // -------------------------
    py::class_<BatchNorm2D>(m, "BatchNorm2D")
        .def(py::init<int>())
        .def("forward", &BatchNorm2D::forward)
        .def_readwrite("gamma", &BatchNorm2D::gamma)
        .def_readwrite("beta", &BatchNorm2D::beta)
        .def_readwrite("running_mean", &BatchNorm2D::running_mean)
        .def_readwrite("running_var", &BatchNorm2D::running_var);

    // -------------------------
    // ReLU
    // -------------------------
    py::class_<ReLU, Module>(m, "ReLU")
        .def(py::init<>())
        .def("forward", &ReLU::forward);

    // -------------------------
    // GeLU
    // -------------------------
    py::class_<GeLU, Module>(m, "GeLU")
        .def(py::init<>())
        .def("forward", &GeLU::forward);

    // -------------------------
    // SoftMax
    // -------------------------
    py::class_<SoftMax, Module>(m, "SoftMax")
        .def(py::init<int>())
        .def("forward", &SoftMax::forward);
}

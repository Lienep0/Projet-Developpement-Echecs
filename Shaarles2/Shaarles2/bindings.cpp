#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "Tensor.hpp"
#include "Conv2D.hpp"
#include "Linear.hpp"
#include "GeLU.hpp"
#include "SoftMax.hpp"
#include "BatchNorm2D.hpp"
#include "ReLU.hpp"
#include "Module.hpp"

namespace py = pybind11;

// Define the Python module

PYBIND11_MODULE(mylib, m) {
    m.doc() = "Mini deep learning library (C++/CUDA)";

    // -------------------------
    // Module, mother of every classes
    // -------------------------
	py::class_<Module>(m, "Module")
		.def("forward", &Module::forward)
		.def("backward", &Module::backward)
		.def("parameters", &Module::parameters);

    // -------------------------
    // Tensor
    // -------------------------
    py::class_<Tensor,Module>(m, "Tensor")
        .def(py::init([](const std::vector<int>& dims) {
        return Tensor(const_cast<int*>(dims.data()), static_cast<int>(dims.size()));
            }))
        .def("zero", &Tensor::zero)
        .def("one", &Tensor::one)
        .def("copy", &Tensor::copy)
        .def("toString", &Tensor::toString)
        .def("getNdim", &Tensor::getNdim)
        .def("getnbEle", &Tensor::getnbEle)
        .def("getDimensions", [](Tensor& t) {
        std::vector<int> dims(t.getNdim());
        for (int i = 0; i < t.getNdim(); ++i)
            dims[i] = t.getDimensions()[i];
        return dims;
            })
        .def("getData", [](Tensor& t) {
        std::vector<float> v(t.getnbEle());
        float* d = t.getData();
        for (int i = 0; i < t.getnbEle(); ++i)
            v[i] = d[i];
        return v;
            });

    // -------------------------
    // Conv2D
    // -------------------------
    py::class_<Conv2D,Module>(m, "Conv2D")
        .def(py::init<int, int, int, int, int>(),
            py::arg("in_channels"),
            py::arg("out_channels"),
            py::arg("kernel_size"),
            py::arg("stride"),
            py::arg("padding"))
        .def("forward", &Conv2D::forward,
            py::arg("input"),
            py::arg("batch_size"),
            py::arg("height"),
            py::arg("width"),
            py::arg("output"));

    // -------------------------
    // Linear
    // -------------------------
    py::class_<Linear, Module>(m, "Linear")
        .def(py::init<int, int>(),
            py::arg("input_size"),
            py::arg("output_size"))
        .def("forward", &Linear::forward,
            py::arg("input"),
            py::arg("output"));

    // -------------------------
    // GeLU
    // -------------------------
    py::class_<GeLU,Module>(m, "GeLU")
        .def(py::init<>())
        .def("forward", &GeLU::forward);


    // -------------------------
    // ReLU
    // -------------------------
    py::class_<ReLU,Module>(m, "ReLU")
        .def(py::init<>())
        .def("forward", &ReLU::forward);

    // -------------------------
    // SoftMax
    // -------------------------
    py::class_<SoftMax,Module>(m, "SoftMax")
        .def(py::init<int>(),
            py::arg("dim"))
        .def("forward", &SoftMax::forward);

    // -------------------------
    // BatchNorm2D
    // -------------------------
    py::class_<BatchNorm2D,Module>(m, "BatchNorm2D")
        .def(py::init<int>(),
            py::arg("num_features"))
        .def("forward", &BatchNorm2D::forward)
        .def("set_training", &BatchNorm2D::set_training)
        .def("is_training", &BatchNorm2D::is_training);
}

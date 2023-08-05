#include "dimredtools_pybind/dimredtools_pybind.hpp"
#include "dimredtools_pybind/docstring/docstring.hpp"

using dim_red::CompressedCoverTree;
using dim_red::CoverTree;
using dim_red::Isomap;
using dim_red::MDS;
using dim_red::docstring::functionDocInject;

PYBIND11_MODULE(dimredtools_pybind, m) {
    m.doc() = "Python binding of DimRedTools";

    py::class_<NearestNeighbors, PyNearestNeighbors>(
        m, "NearestNeighbors",
        "An abstract class for data structures that implement nearest neighbor search.")
        .def("query", &NearestNeighbors::query, "point"_a, "k"_a, "sort_results"_a = true,
             "Retrieves the k-nearest neighbors for the query point.")
        .def("query_radius", &NearestNeighbors::queryRadius, "point"_a, "r"_a,
             "sort_results"_a = false,
             "Retrieves all the neighbors of the query point in the specified radius.");

    py::class_<CoverTree, NearestNeighbors>(m, "CoverTree")
        .def(py::init<const Eigen::Ref<const dim_red::Matrix> &, double, const std::string &>(),
             "x"_a, "base"_a = 1.3, "metric"_a = "euclidean");

    py::class_<CompressedCoverTree, NearestNeighbors>(m, "CompressedCoverTree")
        .def(py::init<const Eigen::Ref<const dim_red::Matrix> &, double, const std::string &>(),
             "x"_a, "base"_a = 1.3, "metric"_a = "euclidean");

    py::class_<MDS>(m, "MDS")
        .def(py::init<int, int, double, double, int, const std::string &>(), "n_components"_a = 2,
             "max_iter"_a = 100, "eps"_a = 1e-4, "learning_rate"_a = 0.2, "random_state"_a = 0,
             "dissimilarity"_a = "euclidean")
        .def("fit_transform", &MDS::fitTransform, "x"_a, "init"_a = std::nullopt, "Fit mapping.")
        .def_readonly("stress_", &MDS::stress_,
                      "Stress function value of the ::fit_transform result.")
        .def_readonly("dissimilarity_matrix_", &MDS::dissimilarity_matrix_,
                      "Matrix of dissimilarities.")
        .def_readonly("n_iter_", &MDS::n_iter_,
                      "Number of iterations of the ::fit_transform algorithm.");

    py::class_<Isomap>(m, "Isomap")
        .def(py::init<std::optional<int>, std::optional<double>, int, int, double, double, int,
                      const std::string &, const std::string &>(),
             "n_neighbors"_a = 5, "radius"_a = std::nullopt, "n_components"_a = 2,
             "max_iter"_a = 100, "eps"_a = 1e-4, "learning_rate"_a = 0.2, "random_state"_a = 0,
             "neighbors_algorithm"_a = "auto", "metric"_a = "euclidean")
        .def("fit_transform", &Isomap::fitTransform, "x"_a, "Fit mapping.")
        .def_readonly("nbrs_", &Isomap::nbrs_, "Stores nearest neighbors instance.")
        .def_readonly("dist_matrix_", &Isomap::dist_matrix_,
                      "Stores the geodesic distance matrix of training data.");
}

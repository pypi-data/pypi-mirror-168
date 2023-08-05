#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

#include "DimRedTools/CoverTree.hpp"
#include "DimRedTools/CompressedCoverTree.hpp"
#include "DimRedTools/MDS.hpp"
#include "DimRedTools/Isomap.hpp"

namespace py = pybind11;
using py::literals::operator""_a;
using dim_red::Matrix;
using dim_red::NearestNeighbors;
using dim_red::Vector;
using dim_red::IntVector;
typedef std::pair<Vector, IntVector> ResultPair;

class PyNearestNeighbors : public NearestNeighbors {
public:
    using NearestNeighbors::NearestNeighbors;

    ResultPair query(const Eigen::Ref<const Vector> &point, int k,
                     bool sort_results) const override {
        PYBIND11_OVERRIDE_PURE(ResultPair, NearestNeighbors, query, point, k, sort_results);
    }
    ResultPair queryRadius(const Eigen::Ref<const Vector> &point, double r,
                           bool sort_results) const override {
        PYBIND11_OVERRIDE_PURE_NAME(ResultPair, NearestNeighbors, "query_radius", queryRadius,
                                    point, r, sort_results);
    }
};

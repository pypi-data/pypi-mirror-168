#include <doctest/doctest.h>
#include <iostream>
#include "DimRedTools/CoverTree.hpp"
#include "DimRedTools/CompressedCoverTree.hpp"
#include "testdata.hpp"

using dim_red::NearestNeighbors;
using dim_red::Matrix;
using dim_red::Vector;
using dim_red::IntVector;
using dim_red::CoverTree;
using dim_red::CompressedCoverTree;

void compare(const NearestNeighbors &test_tree, const NearestNeighbors &correct_tree,
             const Eigen::Ref<Matrix> &x) {
    std::mt19937 generator(0);
    for (int test = 1; test <= 100; ++test) {
        int i = std::uniform_int_distribution(0, static_cast<int>(x.rows()))(generator);
        std::pair<Vector, IntVector> test_answer;
        std::pair<Vector, IntVector> correct_answer;
        if (generator() % 2 == 0) {
            int k = std::uniform_int_distribution(1, static_cast<int>(sqrt(x.rows())))(generator);
            std::cout << "Test " << test << ": " << k << " neighbors..." << std::endl;
            test_answer = test_tree.query(x.row(i), k);
            correct_answer = correct_tree.query(x.row(i), k);
        } else {
            double radius = std::uniform_real_distribution(0.0)(generator);
            std::cout << "Test " << test << ": " << radius << " radius..." << std::endl;
            test_answer = test_tree.queryRadius(x.row(i), radius, true);
            correct_answer = correct_tree.queryRadius(x.row(i), radius, true);
        }
        CHECK(test_answer.first.isApprox(correct_answer.first));
        CHECK((test_answer.second == correct_answer.second));
    }
}

TEST_SUITE("CoverTree") {
    TEST_CASE("InvalidArguments") {
        Matrix empty{};
        CHECK_THROWS(CoverTree(empty));
        Matrix some_matrix{{1, 2, 3}, {4, 5, 6}};
        CoverTree tree(some_matrix);
        CHECK_THROWS(tree.query(Matrix{{0, 0, 0}}, 0));
        CHECK_THROWS(tree.query(Matrix{{0, 0, 0}}, 3));
        CHECK_THROWS(tree.queryRadius(Matrix{{0, 0, 0}}, -1));
    }
    TEST_CASE("Correctness") {
        Matrix data = testDataset(1000, 10);
        compare(CoverTree(data), dim_red::Bruteforce(data), data);
    }
}

TEST_SUITE("CompressedCoverTree") {
    TEST_CASE("InvalidArguments") {
        Matrix empty{};
        CHECK_THROWS(CompressedCoverTree(empty));
        Matrix some_matrix{{1, 2, 3}, {4, 5, 6}};
        CompressedCoverTree tree(some_matrix);
        CHECK_THROWS(tree.query(Matrix{{0, 0, 0}}, 0));
        CHECK_THROWS(tree.query(Matrix{{0, 0, 0}}, 3));
        CHECK_THROWS(tree.queryRadius(Matrix{{0, 0, 0}}, -1));
    }
    /*TEST_CASE("Correctness") {
        Matrix data = testDataset(1000, 10);
        compare(CompressedCoverTree(data), dim_red::Bruteforce(data), data);
    }*/
}

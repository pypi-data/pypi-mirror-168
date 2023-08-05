#include <chrono>
#include <iostream>
#include "doctest/doctest.h"
#include "DimRedTools/CoverTree.hpp"
#include "DimRedTools/CompressedCoverTree.hpp"
#include "../tests/cpp/testdata.hpp"

Matrix data = testDataset(10000, 10);

TEST_CASE("CoverTree_Construction") {
    clock_t clock_1 = clock();
    dim_red::CoverTree tree(data);
    std::cout << static_cast<double>(clock() - clock_1) / CLOCKS_PER_SEC * 1000 << " ms";
}

TEST_CASE("CompressedCoverTree_Construction") {
    clock_t clock_1 = clock();
    dim_red::CompressedCoverTree tree(data);
    std::cout << static_cast<double>(clock() - clock_1) / CLOCKS_PER_SEC * 1000 << " ms";
}

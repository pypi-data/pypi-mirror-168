#include <doctest/doctest.h>
#include "DimRedTools/MDS.hpp"
#include "testdata.hpp"

using dim_red::Matrix;
using dim_red::MDS;

TEST_SUITE("MDS") {
    TEST_CASE("SimpleTest") {
        Matrix data = testDataset(1000, 10);
        Matrix result = MDS().fitTransform(data);
        CHECK_EQ(result.rows(), 1000);
        CHECK_EQ(result.cols(), 2);
    }
}

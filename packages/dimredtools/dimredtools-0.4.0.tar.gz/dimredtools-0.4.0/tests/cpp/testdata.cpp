#include "testdata.hpp"

Matrix testDataset(int samples, int features) {
    std::mt19937 generator(0);
    std::normal_distribution distribution;
    return Matrix::NullaryExpr(samples, features, [&]() { return distribution(generator); });
}

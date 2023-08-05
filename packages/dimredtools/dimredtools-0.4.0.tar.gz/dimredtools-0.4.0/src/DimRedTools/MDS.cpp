#include <iostream>
#include "DimRedTools/MDS.hpp"

namespace dim_red {

MDS::MDS(int n_components, int max_iter, double eps, double learning_rate, int random_state,
         const std::string& dissimilarity)
    : n_components_(n_components),
      max_iter_(max_iter),
      eps_(eps),
      learning_rate_(learning_rate),
      random_(std::mt19937(static_cast<unsigned int>(random_state))),
      dissimilarity_(dissimilarity) {
    if (n_components_ <= 0) {
        throw std::invalid_argument("Invalid number of components: " +
                                    std::to_string(n_components_));
    }
    if (max_iter_ <= 0) {
        throw std::invalid_argument("Invalid maximum number of iterations: " +
                                    std::to_string(n_components_));
    }
    if (eps_ <= 0.0) {
        throw std::invalid_argument("Invalid tolerance: " + std::to_string(n_components_));
    }
    if (learning_rate_ <= 0.0) {
        throw std::invalid_argument("Invalid learning rate: " + std::to_string(n_components_));
    }
    if (dissimilarity_ != "euclidean" && dissimilarity_ != "precomputed") {
        throw std::invalid_argument("Proximity must be 'precomputed' or 'euclidean'. Got " +
                                    dissimilarity_ + " instead");
    }
}

Matrix MDS::euclideanDistances(const Eigen::Ref<const Matrix>& x) const {
    Vector row_norms = x.rowwise().squaredNorm();
    Matrix distances = -2 * x * x.transpose();
    distances.colwise() += row_norms.transpose();
    distances.rowwise() += row_norms;
    return distances;
}

void MDS::validate(const Eigen::Ref<const Matrix>& x,
                   std::optional<const Eigen::Ref<const Matrix>> init) {
    if (dissimilarity_ == "euclidean") {
        dissimilarity_matrix_ = euclideanDistances(x);
    } else if (dissimilarity_ == "precomputed") {
        if (!x.isApprox(x.transpose())) {
            throw std::invalid_argument("Array must be symmetric");
        }
        dissimilarity_matrix_ = x;
    }
    normalizer_ = dissimilarity_matrix_.sum() / 2.0;
    if (init && (init->rows() != x.rows() || init->cols() != n_components_)) {
        throw std::invalid_argument("Init matrix should be of shape (" + std::to_string(x.rows()) +
                                    ", " + std::to_string(n_components_) + ")");
    }
}

Matrix MDS::fitTransform(const Eigen::Ref<const Matrix>& x,
                         std::optional<const Eigen::Ref<const Matrix>> init) {
    validate(x, init);
    std::uniform_real_distribution distribution;
    Matrix x0 = init ? *init : Matrix::NullaryExpr(x.rows(), n_components_, [&]() {
        return distribution(random_);
    });
    Result result = run(x0);
    stress_ = result.stress;
    n_iter_ = result.n_iter;
    return x0;
}

MDS::Result MDS::run(Eigen::Ref<Matrix> x) {
    double step = learning_rate_;
    Matrix x_new(x.rows(), x.cols());
    double stress = getStress(x);
    double past_stress = stress;
    double prev_stress = stress;
    std::cout << "Initial stress = " << stress << std::endl;

    for (int iter = 1; iter <= max_iter_; ++iter) {
        addGradient(x, step, &x_new);
        stress = getStress(x_new);
        if (stress > prev_stress) {
            stress = prev_stress;
            step *= 0.2;
            if (step < eps_) {
                std::cout << "Stopping as stress = " << stress << " after " << iter - 1
                          << " iterations" << std::endl;
                return {stress, iter - 1};
            }
            --iter;
        } else {
            step = std::min(step * 1.5, 0.5);
            prev_stress = stress;

            x_new.rowwise() -= x_new.colwise().mean();
            x = std::move(x_new);

            if (iter % 10 == 0) {
                std::cout << "Stress = " << stress << " after " << iter
                          << " iterations, step = " << step << std::endl;
                if (stress > past_stress - eps_) {
                    return {stress, iter + 1};
                }
                past_stress = stress;
            }
        }
    }
    return {stress, max_iter_};
}

void MDS::addGradient(Eigen::Ref<Matrix> x, double step, Matrix* x_new) const {
    int n = static_cast<int>(x.rows());
    int k = static_cast<int>(x.cols());
    for (int i = 0; i < n; ++i) {
        Array derivative_1 = Vector::Zero(k);
        Array derivative_2 = Vector::Zero(k);
        for (int j = 0; j < n; ++j) {
            if (i == j) {
                continue;
            }
            double d = dissimilarity_matrix_(i, j) == 0.0 ? 1e-10 : dissimilarity_matrix_(i, j);
            Array xv = x.row(i) - x.row(j);
            double d_hat = xv.matrix().norm();
            d_hat = d_hat == 0.0 ? 1e-10 : d_hat;

            double dq = d - d_hat;
            double dr = d * d_hat;
            derivative_1 += xv * dq / dr;
            derivative_2 += (dq - xv * xv * (1.0 + dq / d_hat) / d_hat) / dr;
        }
        x_new->row(i) = x.row(i).array() + step * derivative_1 / derivative_2.abs();
    }
}

double MDS::getStress(Eigen::Ref<Matrix> x) const {
    double stress = 0.0;
    for (int i = 0; i < x.rows(); ++i) {
        for (int j = i + 1; j < x.rows(); ++j) {
            double d = dissimilarity_matrix_(i, j) == 0.0 ? 1e-10 : dissimilarity_matrix_(i, j);
            double d_hat = (x.row(i) - x.row(j)).norm();
            stress += (d - d_hat) * (d - d_hat) / d;
        }
    }
    return stress / normalizer_;
}

}  // namespace dim_red

#ifndef DIMREDTOOLS_INCLUDE_DIMREDTOOLS_MDS_HPP_
#define DIMREDTOOLS_INCLUDE_DIMREDTOOLS_MDS_HPP_

#include "DimRedTools.hpp"
#include <random>
#include <optional>

namespace dim_red {

/**
 * The Sammon's mapping is an iterative technique for making interpoint
 * distances in the low-dimensional projection as close as possible to the
 * interpoint distances in the high-dimensional object. Two points close
 * together in the high-dimensional space should appear close together in the
 * projection, while two points far apart in the high dimensional space should
 * appear far apart in the projection. The Sammon's mapping is a special case of
 * metric least-square multidimensional scaling.
 * <p>
 * Ideally when we project from a high dimensional space to a low dimensional
 * space the image would be geometrically congruent to the original figure.
 * This is called an isometric projection. Unfortunately it is rarely possible
 * to isometrically project objects down into lower dimensional spaces. Instead of
 * trying to achieve equality between corresponding inter-point distances we
 * can minimize the difference between corresponding inter-point distances.
 * This is one goal of the Sammon's mapping algorithm. A second goal of the Sammon's
 * mapping algorithm is to preserve the topology as best as possible by giving
 * greater emphasize to smaller interpoint distances. The Sammon's mapping
 * algorithm has the advantage that whenever it is possible to isometrically
 * project an object into a lower dimensional space it will be isometrically
 * projected into the lower dimensional space. But whenever an object cannot
 * be projected down isometrically the Sammon's mapping projects it down to reduce
 * the distortion in interpoint distances and to limit the change in the
 * topology of the object.
 *
 * <h2>References</h2>
 * <ol>
 * <li> J. W. Sammon. A Nonlinear Mapping for Data Structure Analysis. IEEE 1969. </li>
 * </ol>
 */
class MDS {
public:
    /**
     * @brief Constructor.
     *
     * @param n_components the dimension of the projection.
     * @param max_iter maximum number of iterations.
     * @param eps the tolerance on objective function for stopping iterations, also the tolerance on
     * step size.
     * @param learning_rate initial value of the step size.
     * @param random_state determines the random number generator used to initialize the centers.
     * @param dissimilarity dissimilarity measure to use. 'euclidean': pairwise Euclidean distances
     * between points in the dataset. 'precomputed': pre-computed dissimilarities which are passed
     * to ::fitTransform.
     * @throws std::invalid_argument if any of the first four arguments is <= 0, or if
     * 'dissimilarity' argument is invalid.
     */
    MDS(int n_components = 2, int max_iter = 100, double eps = 1e-4, double learning_rate = 0.2,
        int random_state = 0, const std::string &dissimilarity = "euclidean");

    /**
     * @brief Fit mapping.
     *
     * @param x training data, or matrix of dissimilarities if 'dissimilarity' == 'precomputed'.
     * @param init the initial projected coordinates, of which the column size is the projection
     * dimension.
     * @return the final projected coordinates.
     * @throws std::invalid_argument if dissimilarities are precomputed but the matrix of
     * dissimilarities isn't symmetric, or if 'init' matrix is present but has incorrect shape.
     */
    Matrix fitTransform(const Eigen::Ref<const Matrix> &x,
                        std::optional<const Eigen::Ref<const Matrix>> init = std::nullopt);

    /**
     * Matrix of dissimilarities.
     */
    Matrix dissimilarity_matrix_;
    /**
     * Stress function value of the ::fitTransform result.
     */
    double stress_;
    /**
     * Number of iterations of the ::fitTransform algorithm.
     */
    int n_iter_;

private:
    struct Result {
        double stress;
        int n_iter;

        friend bool operator<(const Result &lhs, const Result &rhs) {
            return lhs.stress < rhs.stress;
        }
    };

    Matrix euclideanDistances(const Eigen::Ref<const Matrix> &x) const;

    void validate(const Eigen::Ref<const Matrix> &x,
                  std::optional<const Eigen::Ref<const Matrix>> init);

    Result run(Eigen::Ref<Matrix> x);

    void addGradient(Eigen::Ref<Matrix> x, double step, Matrix *x_new) const;

    double getStress(Eigen::Ref<Matrix> x) const;

    int n_components_;
    int max_iter_;
    double eps_;
    double learning_rate_;
    std::mt19937 random_;
    std::string dissimilarity_;
    double normalizer_;
};

}  // namespace dim_red

#endif  // DIMREDTOOLS_INCLUDE_DIMREDTOOLS_MDS_HPP_

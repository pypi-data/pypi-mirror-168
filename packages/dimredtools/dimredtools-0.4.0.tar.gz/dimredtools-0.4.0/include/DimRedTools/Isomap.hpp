#ifndef DIMREDTOOLS_INCLUDE_DIMREDTOOLS_ISOMAP_HPP_
#define DIMREDTOOLS_INCLUDE_DIMREDTOOLS_ISOMAP_HPP_

#include "DimRedTools.hpp"
#include <optional>
#include <unordered_set>

namespace dim_red {

/**
 * Isometric feature mapping. Isomap is a widely used low-dimensional embedding methods,
 * where geodesic distances on a weighted graph are incorporated with the
 * classical multidimensional scaling. Isomap is used for computing a
 * quasi-isometric, low-dimensional embedding of a set of high-dimensional
 * data points. Isomap is highly efficient and generally applicable to a broad
 * range of data sources and dimensionalities.
 *
 * <h2>References</h2>
 * <ol>
 * <li> J. B. Tenenbaum, V. de Silva and J. C. Langford  A Global Geometric Framework for Nonlinear
 * Dimensionality Reduction. Science 290(5500):2319-2323, 2000. </li>
 * </ol>
 */
class Isomap {
public:
    /**
     * @brief Constructor.
     *
     * @param n_neighbors the number of nearest neighbors to search for. If present, 'radius' must
     * be std::nullopt.
     * @param radius the nearest neighbors search radius. If present, 'n_neighbors' must be
     * std::nullopt.
     * @param n_components the dimension of the projection.
     * @param max_iter MDS parameter.
     * @param eps MDS parameter.
     * @param learning_rate MDS parameter.
     * @param random_state MDS parameter.
     * @param neighbors_algorithm algorithm to use for nearest neighbors search. Supported: ‘auto’,
     * ‘brute’, ‘cover_tree’
     * @param metric metric for nearest neighbors search.
     */
    Isomap(std::optional<int> n_neighbors = 5, std::optional<double> radius = std::nullopt,
           int n_components = 2, int max_iter = 100, double eps = 1e-4, double learning_rate = 0.2,
           int random_state = 0, const std::string &neighbors_algorithm = "auto",
           const std::string &metric = "euclidean");

    ~Isomap();

    /**
     * @brief Fit mapping.
     *
     * @param x training data.
     * @return the projected coordinates.
     * @throws std::invalid_argument if 'neighbors_algorithm' is unknown, or 'n_neighbors' and
     * 'radius' are incompatible.
     */
    Matrix fitTransform(const Eigen::Ref<const Matrix> &x);

    /**
     * Stores nearest neighbors instance.
     */
    NearestNeighbors *nbrs_;
    /**
     * Stores the geodesic distance matrix of training data.
     */
    Matrix dist_matrix_;

private:
    using Graph = std::vector<std::unordered_set<int>>;

    Graph buildGraph(Eigen::Ref<const Matrix> x);

    void dijkstra(const Graph &graph, int start, Eigen::Ref<Vector> distances) const;

    void dijkstra(const Graph &graph);

    int connectedComponents(const Graph &graph, Eigen::Ref<IntVector> labels) const;

    void fixConnectedComponents(Eigen::Ref<const Matrix> x, int components,
                                Eigen::Ref<IntVector> labels, Graph *graph) const;

    std::optional<int> n_neighbors_;
    std::optional<double> radius_;
    int n_components_;
    int max_iter_;
    double eps_;
    double learning_rate_;
    int random_state_;
    std::string neighbors_algorithm_;
    std::string metric_;
};

}  // namespace dim_red

#endif  // DIMREDTOOLS_INCLUDE_DIMREDTOOLS_ISOMAP_HPP_

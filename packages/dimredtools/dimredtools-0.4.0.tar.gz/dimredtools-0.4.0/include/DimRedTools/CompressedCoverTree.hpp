#ifndef DIMREDTOOLS_INCLUDE_DIMREDTOOLS_COMPRESSEDCOVERTREE_HPP_
#define DIMREDTOOLS_INCLUDE_DIMREDTOOLS_COMPRESSEDCOVERTREE_HPP_

#include "DimRedTools.hpp"
#include <cfloat>
#include <list>

namespace dim_red {

/**
 * A new compressed cover tree guarantees a parameterized time complexity that is near-linear in the
 * maximum size of both query and reference set.
 *
 * <h2>References</h2>
 * <ol>
 * <li> Yury Elkin. New compressed cover tree for k-nearest neighbor search. arXiv 2022. </li>
 * </ol>
 */
class CompressedCoverTree : public NearestNeighbors {
public:
    /**
     * @brief Constructor.
     *
     * @param x the dataset.
     * @param base the base of the expansion constant.
     * @param metric a metric distance measure for nearest neighbor search.
     */
    CompressedCoverTree(const Eigen::Ref<const Matrix> &x, double base = 1.3,
                        const std::string &metric = "euclidean");

    ~CompressedCoverTree();

    std::pair<Vector, IntVector> query(const Eigen::Ref<const Vector> &point, int k,
                                       bool sort_results = true) const override;

    std::pair<Vector, IntVector> queryRadius(const Eigen::Ref<const Vector> &point, double radius,
                                             bool sort_results = false) const override {
        return Bruteforce(data_).queryRadius(point, radius, sort_results);  // TODO
    }

private:
    struct Node {
        const int point;
        const int scale;
        std::list<Node *> *children = new std::list<Node *>;

        Node(const Node &) = delete;
    };

    struct CoverSetEntry {
        const Node *node;
        std::list<Node *>::const_iterator next_child;
    };
    using CoverSet = std::vector<CoverSetEntry>; // TODO: std::unordered_set

    void deleteNode(Node *node) const;

    void build();

    int addPoint(int point) const;

    bool isCovered(int point, int other_point, int scale) const;

    bool isLambdaCovered(const Eigen::Ref<const Vector> &point, int other_point, int lambda,
                         int scale) const;

    void setParent(int point, const CoverSetEntry &parent, int child_scale) const;

    int getScale(double value) const;

    std::pair<const CoverSetEntry &, double> nearestPoint(int point,
                                                          const CoverSet &cover_set) const;

    int countDistinctiveDescendants(const Node *node, int scale,
                                    std::list<Node *>::const_iterator next_child) const;

    void getDistinctiveDescendants(const Node *node, int scale,
                                   std::list<Node *>::const_iterator next_child,
                                   std::vector<int> *result) const;

    int getLambdaPoint(const Eigen::Ref<const Vector> &point, const CoverSet &cover_set, int scale,
                       int k) const;

    template <typename RowIndices>
    std::pair<Vector, IntVector> bruteforceQuery(const RowIndices &indices,
                                                 const Eigen::Ref<const Vector> &point, int k,
                                                 bool sort_results) const;

    const Eigen::Ref<const Matrix> data_;
    std::string metric_;
    Metric distance_;
    double base_;
    double inv_log_base_;
    Node *root_;
    int min_scale_;
};

}  // namespace dim_red

#endif  // DIMREDTOOLS_INCLUDE_DIMREDTOOLS_COMPRESSEDCOVERTREE_HPP_

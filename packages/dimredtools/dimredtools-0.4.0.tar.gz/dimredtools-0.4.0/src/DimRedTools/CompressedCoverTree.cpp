#include "DimRedTools/CompressedCoverTree.hpp"

namespace dim_red {

CompressedCoverTree::CompressedCoverTree(const Eigen::Ref<const Matrix>& x, double base,
                                         const std::string& metric)
    : data_(x),
      metric_(metric),
      distance_(getMetricByName(metric)),
      base_(base),
      inv_log_base_(1.0 / log(base)) {
    if (data_.rows() == 0) {
        throw std::invalid_argument("Dataset is empty");
    }
    build();
}

CompressedCoverTree::~CompressedCoverTree() {
    deleteNode(root_);
}

void CompressedCoverTree::deleteNode(CompressedCoverTree::Node* node) const {
    if (node->children != nullptr) {
        for (const auto& item : *node->children) {
            deleteNode(item);
        }
        delete node->children;
    }
    delete node;
}

void CompressedCoverTree::build() {
    Node* initial_root = new Node{0, INT_MAX};
    root_ = initial_root;
    int max_scale = INT_MIN;
    min_scale_ = INT_MAX;
    for (int i = 1; i < data_.rows(); ++i) {
        int scale = addPoint(i);
        max_scale = std::max(max_scale, scale);
        min_scale_ = std::min(min_scale_, scale);
    }
    root_ = new Node{0, max_scale + 1, initial_root->children};
    delete initial_root;
}

int CompressedCoverTree::addPoint(int point) const {
    int previous_scale = root_->scale;
    int scale = root_->children == nullptr ? INT_MIN : root_->scale - 1;
    CoverSet cover_set{{root_, root_->children->begin()}};

    while (min_scale_ <= scale) {
        CoverSet next_cover_set;

        for (auto& parent : cover_set) {
            auto& next_child = parent.next_child;
            for (; next_child != parent.node->children->end() && (*next_child)->scale >= scale;
                 ++next_child) {
                if ((*next_child)->scale == scale &&
                    isCovered(point, (*next_child)->point, scale)) {
                    next_cover_set.push_back({(*next_child), (*next_child)->children->begin()});
                }
            }

            if (isCovered(point, parent.node->point, scale)) {
                next_cover_set.push_back(parent);
            }
        }

        if (next_cover_set.empty()) {
            setParent(point, nearestPoint(point, cover_set).first, previous_scale);
            return previous_scale;
        }

        int next_scale = min_scale_ - 1;
        for (const auto& item : next_cover_set) {
            if (item.next_child != item.node->children->end()) {
                next_scale = std::max(next_scale, (*item.next_child)->scale);
            }
        }
        previous_scale = scale;
        scale = next_scale;
        cover_set = std::move(next_cover_set);
    }

    auto nearest_point = nearestPoint(point, cover_set);
    int child_scale = std::min(min_scale_ - 1, getScale(nearest_point.second));
    setParent(point, nearest_point.first, child_scale);
    return child_scale;
}

bool CompressedCoverTree::isCovered(int point, int other_point, int scale) const {
    return distance_(data_.row(point), data_.row(other_point)) <= pow(base_, scale + 1);
}

bool CompressedCoverTree::isLambdaCovered(const Eigen::Ref<const Vector>& point, int other_point,
                                          int lambda, int scale) const {
    return distance_(point, data_.row(other_point)) <=
           distance_(point, data_.row(lambda)) + pow(base_, scale + 2);
}

void CompressedCoverTree::setParent(int point, const CompressedCoverTree::CoverSetEntry& parent,
                                    int child_scale) const {
    std::list<Node*>::const_iterator iterator = parent.next_child;
    for (;
         iterator != parent.node->children->begin() && (*std::prev(iterator))->scale < child_scale;
         --iterator) {
    }
    for (; iterator != parent.node->children->end() && (*iterator)->scale >= child_scale;
         ++iterator) {
    }
    parent.node->children->insert(iterator, new Node{point, child_scale});
}

int CompressedCoverTree::getScale(double value) const {
    return static_cast<int>(floor(inv_log_base_ * log(value)));
}

std::pair<const CompressedCoverTree::CoverSetEntry&, double> CompressedCoverTree::nearestPoint(
    int point, const CompressedCoverTree::CoverSet& cover_set) const {
    double min_distance = DBL_MAX;
    size_t nearest_point_index = 0;
    for (size_t i = 0; i < cover_set.size(); ++i) {
        double distance = distance_(data_.row(point), data_.row(cover_set[i].node->point));
        if (distance < min_distance) {
            min_distance = distance;
            nearest_point_index = i;
        }
    }
    return {cover_set[nearest_point_index], min_distance};
}

int CompressedCoverTree::countDistinctiveDescendants(
    const CompressedCoverTree::Node* node, int scale,
    std::list<CompressedCoverTree::Node*>::const_iterator next_child) const {
    int result = 0;
    if (scale > min_scale_) {
        for (; next_child != node->children->end() && (*next_child)->scale >= scale - 1;
             ++next_child) {
            if ((*next_child)->scale == scale - 1) {
                result += countDistinctiveDescendants(
                    *next_child,
                    (*next_child)->children->empty() ? min_scale_
                                                     : 1 + (*next_child)->children->front()->scale,
                    (*next_child)->children->begin());
            }
        }
        result += countDistinctiveDescendants(
            node, next_child == node->children->end() ? min_scale_ : 1 + (*next_child)->scale,
            next_child);
    } else {
        ++result;
    }
    return result;
}

void CompressedCoverTree::getDistinctiveDescendants(
    const CompressedCoverTree::Node* node, int scale,
    std::list<CompressedCoverTree::Node*>::const_iterator next_child,
    std::vector<int>* result) const {
    assert(std::find(result->begin(), result->end(), node->point) == result->end());
    result->push_back(node->point);
    if (scale > min_scale_) {
        int next_scale =
            next_child == node->children->end() ? min_scale_ - 1 : (*next_child)->scale;
        for (; next_child != node->children->end() && (*next_child)->scale == next_scale;
             ++next_child) {
            getDistinctiveDescendants(*next_child, (*next_child)->scale,
                                      (*next_child)->children->begin(), result);
        }
    }
}

int CompressedCoverTree::getLambdaPoint(const Eigen::Ref<const Vector>& point,
                                        const CompressedCoverTree::CoverSet& cover_set, int scale,
                                        int k) const {
    NeighborsHeap<std::pair<double, const Node*>> heap(static_cast<size_t>(k));
    for (const CoverSetEntry& item : cover_set) {
        heap.add({distance_(data_.row(item.node->point), point), item.node});
    }
    auto neighbors = heap.extract();
    int sum = 0;
    size_t index;
    for (index = 0; index < neighbors.size() - 1; ++index) {
        const Node* node = neighbors[index].second;
        sum += countDistinctiveDescendants(node, scale, node->children->begin());
        if (sum >= k) {
            break;
        }
    }
    return static_cast<int>(index);
}

std::pair<Vector, IntVector> CompressedCoverTree::query(const Eigen::Ref<const Vector>& point,
                                                        int k, bool sort_results) const {
    validate(static_cast<int>(data_.rows()), k, 0.0, true);

    int scale = root_->children == nullptr ? INT_MIN : root_->scale - 1;
    static CoverSet cover_set{{root_, root_->children->begin()}};

    while (min_scale_ <= scale) {
        CoverSet next_cover_set;

        for (auto& parent : cover_set) {
            auto& next_child = parent.next_child;
            for (; next_child != parent.node->children->end() && (*next_child)->scale >= scale;
                 ++next_child) {
                if ((*next_child)->scale == scale) {
                    next_cover_set.push_back({(*next_child), (*next_child)->children->begin()});
                }
            }
            next_cover_set.push_back(parent);
        }

        int lambda = getLambdaPoint(point, next_cover_set, scale, k);
        std::remove_if(next_cover_set.begin(), next_cover_set.end(), [&](auto& entry) {
            return !isLambdaCovered(point, entry.node->point, lambda, scale);
        });

        if (distance_(point, data_.row(lambda)) > pow(2, scale + 2)) {
            std::vector<int> candidates;
            for (const auto& item : next_cover_set) {
                getDistinctiveDescendants(item.node, scale, item.next_child, &candidates);
            }
            return bruteforceQuery(candidates, point, k, sort_results);
        }

        int next_scale = min_scale_ - 1;
        for (const auto& item : next_cover_set) {
            if (item.next_child != item.node->children->end()) {
                next_scale = std::max(next_scale, (*item.next_child)->scale);
            }
        }
        scale = next_scale;
        cover_set = std::move(next_cover_set);
    }

    struct Candidates {
        Eigen::Index size() const {
            return static_cast<Eigen::Index>(cover_set.size());
        }
        Eigen::Index operator[](Eigen::Index i) const {
            return cover_set[static_cast<size_t>(i)].node->point;
        }
    };
    return bruteforceQuery(Candidates{}, point, k, sort_results);
}

template <typename RowIndices>
std::pair<Vector, IntVector> CompressedCoverTree::bruteforceQuery(
    const RowIndices& indices, const Eigen::Ref<const Vector>& point, int k,
    bool sort_results) const {
    std::pair<Vector, IntVector> result =
        Bruteforce(data_(indices, Eigen::all), metric_).query(point, k, sort_results);
    for (auto& item : result.second) {
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wsign-conversion"
        item = static_cast<int>(indices[item]);
#pragma clang diagnostic pop
    }
    return result;
}

}  // namespace dim_red

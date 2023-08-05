#include "DimRedTools/Isomap.hpp"
#include "DimRedTools/CoverTree.hpp"
#include "DimRedTools/MDS.hpp"

namespace dim_red {

Isomap::Isomap(std::optional<int> n_neighbors, std::optional<double> radius, int n_components,
               int max_iter, double eps, double learning_rate, int random_state,
               const std::string& neighbors_algorithm, const std::string& metric)
    : n_neighbors_(n_neighbors),
      radius_(radius),
      n_components_(n_components),
      max_iter_(max_iter),
      eps_(eps),
      learning_rate_(learning_rate),
      random_state_(random_state),
      neighbors_algorithm_(neighbors_algorithm),
      metric_(metric) {
}

Isomap::~Isomap() {
    delete nbrs_;
}

Matrix Isomap::fitTransform(const Eigen::Ref<const Matrix>& x) {
    Graph graph = buildGraph(x);
    IntVector labels(x.rows());
    int connected_components = connectedComponents(graph, labels);
    fixConnectedComponents(x, connected_components, labels, &graph);
    dijkstra(graph);  // TODO: support of precomputed distances
    return MDS(n_components_, max_iter_, eps_, learning_rate_, random_state_, metric_)
        .fitTransform(dist_matrix_);
}

Isomap::Graph Isomap::buildGraph(Eigen::Ref<const Matrix> x) {
    if (neighbors_algorithm_ == "auto" || neighbors_algorithm_ == "cover_tree") {
        nbrs_ = new CoverTree(x, 1.3, metric_);
    } else if (neighbors_algorithm_ == "brute") {
        nbrs_ = new Bruteforce(x, metric_);
    } else {
        throw std::invalid_argument("Unknown algorithm for nearest neighbors search: " + metric_);
    }
    if (n_neighbors_.has_value() == radius_.has_value()) {
        throw std::invalid_argument(
            "Only one of 'n_neighbors' and 'radius' arguments must be provided");
    }

    int n = static_cast<int>(x.rows());
    Graph graph(static_cast<size_t>(n));
    for (int i = 0; i < n; ++i) {
        IntVector indices =
            (n_neighbors_
                 ? nbrs_->query(x.row(static_cast<int64_t>(i)), n_neighbors_.value(), false)
                 : nbrs_->queryRadius(x.row(static_cast<int64_t>(i)), radius_.value()))
                .second;
        for (const auto& index : indices) {
            if (index != i) {
                graph[static_cast<size_t>(i)].insert(index);
                graph[static_cast<size_t>(index)].insert(i);
            }
        }
    }
    return graph;
}

void Isomap::dijkstra(const Graph& graph, int start, Eigen::Ref<Vector> distances) const {
    distances.setConstant(DBL_MAX);
    distances[start] = 0;
    std::priority_queue<std::pair<int, size_t>> queue;
    queue.push({0, start});
    while (!queue.empty()) {
        size_t vertex = queue.top().second;
        int distance = -queue.top().first;
        queue.pop();
        if (distance > distances[static_cast<int64_t>(vertex)]) {
            continue;
        }
        for (const auto& to : graph[vertex]) {
            if (distances[static_cast<int64_t>(vertex)] + 1 < distances[to]) {
                distances[to] = distances[static_cast<int64_t>(vertex)] + 1;
                queue.push({-distances[to], to});
            }
        }
    }
}

void Isomap::dijkstra(const Graph& graph) {
    int n = static_cast<int>(graph.size());
    dist_matrix_.resize(n, n);
    for (int i = 0; i < n; ++i) {
        dijkstra(graph, i, dist_matrix_.row(i));
    }
}

int Isomap::connectedComponents(const Graph& graph, Eigen::Ref<IntVector> labels) const {
    int n = static_cast<int>(graph.size());
    labels.setConstant(-1);
    int current_label = 0;
    std::queue<int> no_label;
    for (int i = 0; i < n; ++i) {
        if (labels[i] == -1) {
            no_label.push(i);
            while (!no_label.empty()) {
                int vertex = no_label.front();
                no_label.pop();
                labels[vertex] = current_label;
                for (const int& to : graph[static_cast<size_t>(vertex)]) {
                    if (labels[to] == -1) {
                        no_label.push(to);
                    }
                }
            }
            ++current_label;
        }
    }
    return current_label;
}

void Isomap::fixConnectedComponents(Eigen::Ref<const Matrix> x, int components,
                                    Eigen::Ref<IntVector> labels, Graph* graph) const {
    int n = static_cast<int>(x.rows());
    Metric distance = getMetricByName(metric_);
    for (int i = 0; i < components; ++i) {
        for (int j = 0; j < components; ++j) {
            if (i == j) {
                continue;
            }
            double min_distance = DBL_MAX;
            int min_from;
            int min_to;
            for (int from = 0; from < n; ++from) {
                if (labels[from] != i) {
                    continue;
                }
                for (int to = 0; to < n; ++to) {
                    if (labels[to] != j) {
                        continue;
                    }
                    double current_distance = distance(x.row(from), x.row(to));
                    if (current_distance < min_distance) {
                        min_distance = current_distance;
                        min_from = from;
                        min_to = to;
                    }
                }
            }
            (*graph)[static_cast<size_t>(min_from)].insert(min_to);
            (*graph)[static_cast<size_t>(min_to)].insert(min_from);
        }
    }
}

}  // namespace dim_red

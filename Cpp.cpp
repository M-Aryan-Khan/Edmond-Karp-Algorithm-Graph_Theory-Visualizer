#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <algorithm>
#include <random>
#include <chrono>
#include <cstdlib>
#include <unistd.h>

class EdmondsKarp {
private:
    int V;
    std::vector<std::vector<int>> capacity;
    std::vector<std::vector<int>> adj;

    bool bfs(int s, int t, std::vector<int>& parent) {
        std::vector<bool> visited(V, false);
        std::queue<int> q;
        q.push(s);
        visited[s] = true;
        parent[s] = -1;

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int v : adj[u]) {
                if (!visited[v] && capacity[u][v] > 0) {
                    q.push(v);
                    parent[v] = u;
                    visited[v] = true;

                    if (v == t)
                        return true;
                }
            }
        }

        return false;
    }

public:
    EdmondsKarp(int vertices) : V(vertices) {
        capacity.resize(V, std::vector<int>(V, 0));
        adj.resize(V);
    }

    void addEdge(int u, int v, int cap) {
        adj[u].push_back(v);
        adj[v].push_back(u);
        capacity[u][v] = cap;
    }

    int maxFlow(int s, int t) {
        int max_flow = 0;
        std::vector<int> parent(V);

        while (bfs(s, t, parent)) {
            int path_flow = std::numeric_limits<int>::max();

            for (int v = t; v != s; v = parent[v]) {
                int u = parent[v];
                path_flow = std::min(path_flow, capacity[u][v]);
            }

            for (int v = t; v != s; v = parent[v]) {
                int u = parent[v];
                capacity[u][v] -= path_flow;
                capacity[v][u] += path_flow;
            }

            max_flow += path_flow;
        }

        return max_flow;
    }
};

int main() {
    // Seed for random number generation
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine generator(seed);

    auto start_time = std::chrono::high_resolution_clock::now();

    // Array of possible node counts
    std::vector<int> nodeCounts = {10, 15, 20, 25, 30};

    // Randomly select a node count
    std::uniform_int_distribution<int> distribution(0, nodeCounts.size() - 1);
    int selectedNodeCount = nodeCounts[distribution(generator)];
    std::cout << "Randomly selected node count: " << selectedNodeCount << std::endl;

    // Create the graph with the selected number of nodes
    EdmondsKarp graph(selectedNodeCount);

    // Create two edge sets for each possible node count
    std::vector<std::vector<std::vector<std::vector<int>>>> edgeSets = {
        { // 10 nodes
            {
                {0, 1, 10}, {1, 2, 8}, {2, 3, 5}, {3, 4, 7}, {4, 5, 6},
                {5, 6, 4}, {6, 7, 9}, {7, 8, 3}, {8, 9, 5}, {0, 9, 2},
                {1, 5, 4}, {2, 6, 3}, {3, 7, 6}, {4, 8, 5}, {0, 5, 7}
            },
            {
                {0, 2, 7}, {2, 4, 5}, {4, 6, 8}, {6, 8, 6}, {8, 1, 4},
                {1, 3, 9}, {3, 5, 3}, {5, 7, 5}, {7, 9, 7}, {9, 0, 2},
                {0, 7, 6}, {1, 8, 3}, {2, 9, 4}, {3, 6, 5}, {4, 5, 8}
            }
        },
        { // 15 nodes
            {
                {0, 1, 12}, {1, 2, 10}, {2, 3, 8}, {3, 4, 9}, {4, 5, 7},
                {5, 6, 11}, {6, 7, 6}, {7, 8, 8}, {8, 9, 5}, {9, 10, 7},
                {10, 11, 9}, {11, 12, 6}, {12, 13, 8}, {13, 14, 10}, {0, 14, 5},
                {1, 7, 7}, {2, 8, 6}, {3, 9, 5}, {4, 10, 8}, {5, 11, 7},
                {6, 12, 9}, {7, 13, 6}, {8, 14, 8}, {0, 10, 4}, {1, 11, 5}
            },
            {
                {0, 3, 9}, {3, 6, 7}, {6, 9, 8}, {9, 12, 6}, {12, 0, 5},
                {1, 4, 11}, {4, 7, 8}, {7, 10, 7}, {10, 13, 9}, {13, 1, 6},
                {2, 5, 10}, {5, 8, 6}, {8, 11, 8}, {11, 14, 7}, {14, 2, 5},
                {0, 8, 7}, {1, 9, 6}, {2, 10, 8}, {3, 11, 5}, {4, 12, 7},
                {5, 13, 9}, {6, 14, 6}, {7, 0, 8}, {8, 1, 5}, {9, 2, 7}
            }
        },
        { // 20 nodes
            {
                {0, 1, 15}, {1, 2, 12}, {2, 3, 10}, {3, 4, 8}, {4, 5, 11},
                {5, 6, 9}, {6, 7, 13}, {7, 8, 7}, {8, 9, 10}, {9, 10, 6},
                {10, 11, 8}, {11, 12, 12}, {12, 13, 9}, {13, 14, 11}, {14, 15, 7},
                {15, 16, 10}, {16, 17, 8}, {17, 18, 9}, {18, 19, 11}, {0, 19, 6},
                {1, 10, 8}, {2, 11, 7}, {3, 12, 9}, {4, 13, 6}, {5, 14, 8},
                {6, 15, 7}, {7, 16, 10}, {8, 17, 6}, {9, 18, 9}, {10, 19, 7}
            },
            {
                {0, 4, 11}, {4, 8, 9}, {8, 12, 8}, {12, 16, 10}, {16, 19, 7},
                {1, 5, 13}, {5, 9, 7}, {9, 13, 11}, {13, 17, 8}, {17, 0, 9},
                {2, 6, 10}, {6, 10, 8}, {10, 14, 9}, {14, 18, 7}, {18, 1, 11},
                {3, 7, 12}, {7, 11, 9}, {11, 15, 8}, {15, 19, 10}, {19, 2, 6},
                {0, 10, 8}, {1, 11, 7}, {2, 12, 9}, {3, 13, 6}, {4, 14, 10},
                {5, 15, 7}, {6, 16, 9}, {7, 17, 8}, {8, 18, 6}, {9, 19, 11}
            }
        },
        { // 25 nodes
            {
                {0, 1, 18}, {1, 2, 15}, {2, 3, 12}, {3, 4, 10}, {4, 5, 14},
                {5, 6, 11}, {6, 7, 16}, {7, 8, 9}, {8, 9, 13}, {9, 10, 8},
                {10, 11, 10}, {11, 12, 15}, {12, 13, 11}, {13, 14, 14}, {14, 15, 9},
                {15, 16, 12}, {16, 17, 10}, {17, 18, 11}, {18, 19, 13}, {19, 20, 8},
                {20, 21, 10}, {21, 22, 12}, {22, 23, 9}, {23, 24, 11}, {0, 24, 7},
                {1, 12, 9}, {2, 13, 8}, {3, 14, 10}, {4, 15, 7}, {5, 16, 9},
                {6, 17, 8}, {7, 18, 11}, {8, 19, 7}, {9, 20, 10}, {10, 21, 8}
            },
            {
                {0, 5, 14}, {5, 10, 11}, {10, 15, 10}, {15, 20, 12}, {20, 0, 9},
                {1, 6, 16}, {6, 11, 9}, {11, 16, 13}, {16, 21, 10}, {21, 1, 11},
                {2, 7, 12}, {7, 12, 10}, {12, 17, 11}, {17, 22, 9}, {22, 2, 13},
                {3, 8, 15}, {8, 13, 11}, {13, 18, 10}, {18, 23, 12}, {23, 3, 8},
                {4, 9, 13}, {9, 14, 10}, {14, 19, 12}, {19, 24, 9}, {24, 4, 11},
                {0, 12, 10}, {1, 13, 9}, {2, 14, 11}, {3, 15, 8}, {4, 16, 12},
                {5, 17, 9}, {6, 18, 11}, {7, 19, 10}, {8, 20, 8}, {9, 21, 13}
            }
        },
        { // 30 nodes
            {
                {0, 1, 20}, {1, 2, 17}, {2, 3, 14}, {3, 4, 12}, {4, 5, 16},
                {5, 6, 13}, {6, 7, 18}, {7, 8, 11}, {8, 9, 15}, {9, 10, 10},
                {10, 11, 12}, {11, 12, 17}, {12, 13, 13}, {13, 14, 16}, {14, 15, 11},
                {15, 16, 14}, {16, 17, 12}, {17, 18, 13}, {18, 19, 15}, {19, 20, 10},
                {20, 21, 12}, {21, 22, 14}, {22, 23, 11}, {23, 24, 13}, {24, 25, 9},
                {25, 26, 11}, {26, 27, 13}, {27, 28, 10}, {28, 29, 12}, {0, 29, 8},
                {1, 15, 11}, {2, 16, 10}, {3, 17, 12}, {4, 18, 9}, {5, 19, 11},
                {6, 20, 10}, {7, 21, 13}, {8, 22, 9}, {9, 23, 12}, {10, 24, 10}
            },
            {
                {0, 6, 16}, {6, 12, 13}, {12, 18, 12}, {18, 24, 14}, {24, 29, 11},
                {1, 7, 18}, {7, 13, 11}, {13, 19, 15}, {19, 25, 12}, {25, 0, 13},
                {2, 8, 14}, {8, 14, 12}, {14, 20, 13}, {20, 26, 11}, {26, 1, 15},
                {3, 9, 17}, {9, 15, 13}, {15, 21, 12}, {21, 27, 14}, {27, 2, 10},
                {4, 10, 15}, {10, 16, 12}, {16, 22, 14}, {22, 28, 11}, {28, 3, 13},
                {5, 11, 16}, {11, 17, 11}, {17, 23, 13}, {23, 29, 10}, {29, 4, 12},
                {0, 14, 12}, {1, 15, 11}, {2, 16, 13}, {3, 17, 10}, {4, 18, 14},
                {5, 19, 11}, {6, 20, 13}, {7, 21, 12}, {8, 22, 10}, {9, 23, 15}
            }
        }
    };

    // Randomly select one of the edge sets for the chosen node count
    std::uniform_int_distribution<int> edgeSetDistribution(0, 1);
    int selectedEdgeSetIndex = edgeSetDistribution(generator);
    std::cout << "Randomly selected edge set: " << (selectedEdgeSetIndex + 1) << std::endl;

    // Add edges from the selected edge set to the graph
    for (const auto& edge : edgeSets[std::distance(nodeCounts.begin(), std::find(nodeCounts.begin(), nodeCounts.end(), selectedNodeCount))][selectedEdgeSetIndex]) {
        graph.addEdge(edge[0], edge[1], edge[2]);
    }

    int source = 0;
    int sink = selectedNodeCount - 1;

    int maxFlow = graph.maxFlow(source, sink);
    std::cout << "Maximum flow from source (" << source << ") to sink (" << sink << "): " << maxFlow << std::endl << std::endl;

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    std::cout << "Execution Time: " << elapsed.count() << " seconds" << std::endl;
    
    long rss = 0L;
    FILE* fp = NULL;
    if ((fp = fopen("/proc/self/statm", "r")) == NULL)
        std::cerr << "Can't open statm file" << std::endl;
    if (fscanf(fp, "%*s%ld", &rss) != 1) {
        std::cerr << "Can't read memory usage" << std::endl;
    }
    fclose(fp);
    long page_size = sysconf(_SC_PAGESIZE);
    double memory_usage = rss * page_size / 1024.0 / 1024.0; // Convert to MB

    std::cout << "Memory Usage: " << memory_usage << " MB" << std::endl;

    return 0;
}
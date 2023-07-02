import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def create_edge_list(weight, n):
    edge_list = []
    for i in range(n):
        for j in range(n):
            edge = [i, j, weight[i][j]]
            edge_list.append(edge)
    return edge_list


def draw_graph(graph, points):
    positions = {}
    for i in range(points.index.size):
        positions.update({i: (points.at[i, 'X'], points.at[i, 'Y'])})
    nx.draw(graph, pos=positions, node_size=10, nodelist=positions.keys(), with_labels=positions)


def minimum_spanning_tree(n_vertex, weight):
    g = nx.Graph()
    edge_list = create_edge_list(weight, n_vertex)
    for edge in edge_list:
        g.add_edge(edge[0], edge[1], weight=edge[2])
    tree = nx.minimum_spanning_tree(g)
    print(tree.edges(data=True))
    return tree


def delete_edge(tree):
    g = nx.Graph()
    sum = 0
    count = 0
    for (u, v, d) in tree.edges(data=True):
        sum += d['weight']
        count += 1
    max_weight = sum / count
    for (u, v, d) in tree.edges(data=True):
        if d['weight'] < max_weight:
            g.add_edge(u, v, weight=d)
    return g


def definition_clusters(graph):
    clusters = []
    edges = list(graph.edges)
    print(edges)
    i: int = 0
    while i < len(edges):
        vertexes = [edges[i][0], edges[i][1]]
        edges.remove((edges[i][0], edges[i][1]))
        j: int = 0
        while j < len(edges):
            if edges[j][0] in vertexes:
                vertexes.append(edges[j][1])
                edges.remove((edges[j][0], edges[j][1]))
                j = 0
            elif edges[j][1] in vertexes:
                vertexes.append(edges[j][0])
                edges.remove((edges[j][0], edges[j][1]))
                j = 0
            else:
                j = j + 1
        clusters.append(vertexes)
    print(len(clusters))
    print(clusters)
    return clusters


def calculate_centroids(clusters, points):
    centroids = pd.DataFrame(columns=['X', 'Y'])
    k = 0
    for item in clusters:
        mean_x = 0
        mean_y = 0
        for i in item:
            mean_x += points.at[i, 'X']
            mean_y += points.at[i, 'Y']
        x = mean_x / len(item)
        y = mean_y / len(item)
        centroids.loc[k] = {'X': x, 'Y': y}

        k += 1
    return centroids


def minimal_spanning_tree_clustering(n_figure, weight, points):
    n_points = points.index.size
    plt.figure(n_figure)
    tree = minimum_spanning_tree(n_points, weight)
    #draw_graph(tree, points)
    plt.figure(n_figure)
    tree = delete_edge(tree)
    # draw_graph(tree, points)
    clusters = definition_clusters(tree)
    centroids = calculate_centroids(clusters, points)
    return centroids

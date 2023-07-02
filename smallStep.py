import pandas as pd
import k_means
import matplotlib.pyplot as plt


def small_step(points, max_radius, n_figure):
    n_points = points.index.size
    centroids = pd.DataFrame(columns=['X', 'Y'])
    distances = k_means.calculate_distance_points(points)
    points_clusters: list[float] = [-1 for i in range(n_points)]
    while True:
        min_i, min_j = k_means.min_distance(distances, n_points, n_points)
        number_cluster = centroids.index.size
        if min_i == -1 or min_j == -1:
            break
        if points_clusters[min_i] == -1 and points_clusters[min_j] == -1 and distances[min_i][min_j] <= 2 * max_radius:
            x = (points.at[min_i, 'X'] + points.at[min_j, 'X']) / 2
            y = (points.at[min_i, 'Y'] + points.at[min_j, 'Y']) / 2
            centroids.loc[number_cluster] = {'X': x, 'Y': y}
            points_clusters[min_i] = number_cluster
            points_clusters[min_j] = number_cluster

        elif points_clusters[min_i] != -1 and points_clusters[min_j] == -1:
            points_clusters = add_point(points, centroids, points_clusters, min_j, points_clusters[min_i], max_radius)

        elif points_clusters[min_i] == -1 and points_clusters[min_j] != -1:
            points_clusters = add_point(points, centroids, points_clusters, min_i, points_clusters[min_j], max_radius)

        elif points_clusters[min_i] != -1 and points_clusters[min_j] != -1 and points_clusters[min_i] != \
                points_clusters[min_j]:
            centroids, points_clusters = change_cluster(points, centroids, min_i, min_j, points_clusters, max_radius)
        distances[min_i][min_j] = -1.0
        distances[min_j][min_i] = -1.0
    print(points_clusters)
    draw_clustering(n_figure, points, centroids, points_clusters)
    return centroids


def add_point(list_points, list_centroids, points_cluster, index_point, n_cluster, max_radius):
    x = list_points.at[index_point, 'X']
    y = list_points.at[index_point, 'Y']
    count = 1
    for i in range(list_points.index.size):
        if points_cluster[i] == n_cluster:
            x += list_points.at[i, 'X']
            y += list_points.at[i, 'Y']
            count += 1
    x = x / count
    y = y / count

    points_cluster[index_point] = n_cluster
    flag = True
    for i in range(list_points.index.size):
        if points_cluster[i] == n_cluster:
            if k_means.evclid_distance(x, y, list_points.at[i, 'X'], list_points.at[i, 'Y']) > max_radius:
                flag = False
                break

    if flag:
        list_centroids.at[n_cluster, 'X'] = x
        list_centroids.at[n_cluster, 'Y'] = y
    else:
        points_cluster[index_point] = -1
    return points_cluster


def change_cluster(list_points, list_centroids, index1, index2, points_clusters, max_radius):
    x = 0.0
    y = 0.0
    count = 0
    for i in range(list_points.index.size):
        if points_clusters[i] == points_clusters[index1] or points_clusters[i] == points_clusters[index2]:
            x += list_points.at[i, 'X']
            y += list_points.at[i, 'Y']
            count += 1
    x = x / count
    y = y / count

    flag = True
    for i in range(list_points.index.size):
        if points_clusters[i] == points_clusters[index1] or points_clusters[i] == points_clusters[index2]:
            if k_means.evclid_distance(x, y, list_points.at[i, 'X'], list_points.at[i, 'Y']) > max_radius:
                flag = False
                break
    if flag:
        if points_clusters[index1] > points_clusters[index2]:
            list_centroids.at[points_clusters[index2], 'X'] = x
            list_centroids.at[points_clusters[index2], 'Y'] = y
            list_centroids = pd.DataFrame(list_centroids.drop(index=[points_clusters[index1]]))
            list_centroids.reset_index(drop=True, inplace=True)
            index = points_clusters[index1]
            for i in range(list_points.index.size):
                if points_clusters[i] == index:
                    points_clusters[i] = points_clusters[index2]
                if points_clusters[i] > index:
                    points_clusters[i] = points_clusters[i] - 1

        else:
            list_centroids.at[points_clusters[index1], 'X'] = x
            list_centroids.at[points_clusters[index1], 'Y'] = y
            list_centroids = pd.DataFrame(list_centroids.drop(index=[points_clusters[index2]]))
            list_centroids.reset_index(drop=True, inplace=True)
            index = points_clusters[index2]
            for i in range(list_points.index.size):
                if points_clusters[i] == index:
                    points_clusters[i] = points_clusters[index1]
                if points_clusters[i] > index:
                    points_clusters[i] = points_clusters[i] - 1
    return list_centroids, points_clusters


def draw_clustering(number_figure, list_points, list_clusters, list_point_cluster=None):
    n = list_points.index.size
    plt.figure(number_figure)
    # if number_figure != 1:
    for i in range(n):
        if list_point_cluster[i] != -1:
            plt.plot([list_points.at[i, 'X'], list_clusters.at[list_point_cluster[i], 'X']],
                     [list_points.at[i, 'Y'], list_clusters.at[list_point_cluster[i], 'Y']], 'y',
                     linewidth=3, zorder=0)
    plt.scatter(list_points['X'], list_points['Y'], c='red', s=20, zorder=1)
    plt.scatter(list_clusters['X'], list_clusters['Y'], c='green', s=30, marker=(5, 2), zorder=1)

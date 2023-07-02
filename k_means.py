import pandas as pd
import numpy as np


def points_generation(n_points, start_x, exd_x, start_y, end_y):
    points = pd.DataFrame({'X': np.random.uniform(start_x, exd_x, n_points),
                           'Y': np.random.uniform(start_y, end_y, n_points)})
    points.to_excel('Data/points.xlsx')


def centroids_generation(n_clusters, start_x, exd_x, start_y, end_y):
    centroids = pd.DataFrame({'X': np.random.uniform(start_x, exd_x, n_clusters),
                              'Y': np.random.uniform(start_y, end_y, n_clusters)})

    centroids.to_excel('Data/centroids.xlsx')


def evclid_distance(x1, y1, x2, y2):
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2), 1 / 2)


def search_index(index, index_const_clusters):
    for i in range(len(index_const_clusters)):
        if index == index_const_clusters[i]:
            return True
    return False


def calculate_distance(list_points, list_clusters):
    n = list_clusters.index.size
    m = list_points.index.size
    distance = [[0] * m for i in range(n)]
    for i in range(n):
        for j in range(m):
            distance[i][j] = evclid_distance(list_points.at[j, 'X'], list_points.at[j, 'Y'],
                                             list_clusters.at[i, 'X'], list_clusters.at[i, 'Y'])
    return distance


def cluster_distribution(distances, max_distance, n, m):
    point_cluster = [[-1] * m for i in range(n)]
    for j in range(m):
        min_distance = distances[0][j]
        cluster_i = -1
        for i in range(n):
            if max_distance != -1:
                if distances[i][j] <= min_distance and distances[i][j] <= max_distance:
                    min_distance = distances[i][j]
                    cluster_i = i
            else:
                if distances[i][j] <= min_distance:
                    min_distance = distances[i][j]
                    cluster_i = i

        if cluster_i != -1:
            point_cluster[cluster_i][j] = cluster_i
    return point_cluster


def recalculation_centroids(points, point_cluster, clusters, index_const_clusters):
    n = clusters.index.size
    m = points.index.size
    for i in range(n):
        if search_index(i, index_const_clusters):
            continue
        mean_x = 0
        mean_y = 0
        count = 0
        for j in range(m):
            if point_cluster[i][j] == i:
                mean_x += points.at[j, 'X']
                mean_y += points.at[j, 'Y']
                count = count + 1
        if count != 0:
            clusters.at[i, 'X'] = mean_x / count
            clusters.at[i, 'Y'] = mean_y / count


def compare_array(array1, array2, n, m):
    for i in range(n):
        for j in range(m):
            if array1[i][j] != array2[i][j]:
                return False
    return True


def find_index_outside_point(point_cluster, n, m):
    point_j = -1
    for j in range(m):
        k = 0
        for i in range(n):
            if point_cluster[i][j] != -1:
                k = 1
        if k == 0:
            point_j = j
            break
    return point_j


# calculate distances between points
def calculate_distance_points(list_points):
    m = list_points.index.size
    distance = [[0] * m for i in range(m)]
    for i in range(m):
        for j in range(m):
            distance[i][j] = evclid_distance(list_points.at[j, 'X'], list_points.at[j, 'Y'],
                                             list_points.at[i, 'X'], list_points.at[i, 'Y'])
    return distance


# calculate distances between centroids
def calculate_distance_centroids(list_centroids):
    n = list_centroids.index.size
    distance = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distance[i][j] = evclid_distance(list_centroids.at[j, 'X'], list_centroids.at[j, 'Y'],
                                             list_centroids.at[i, 'X'], list_centroids.at[i, 'Y'])
            distance[j][i] = distance[i][j]
    return distance


# search min distances between centroids
def min_distance(list_distance, n, m):
    min_dist = -1
    min_i = -1
    min_j = -1
    for i in range(n):
        for j in range(0, m):
            if min_dist >= list_distance[i][j] > 0 or (min_dist == -1 and list_distance[i][j] > 0):
                min_dist = list_distance[i][j]
                min_i = i
                min_j = j
    return min_i, min_j


def delete_centroid(list_centroids, centroid1, centroid2, list_const_centroid):
    x = (list_centroids.at[centroid1, 'X'] + list_centroids.at[centroid2, 'X']) / 2
    y = (list_centroids.at[centroid1, 'Y'] + list_centroids.at[centroid2, 'Y']) / 2
    list_centroids.at[centroid1, 'X'] = x
    list_centroids.at[centroid1, 'Y'] = y
    for i in range(len(list_const_centroid)):
        if list_const_centroid[i] >= centroid2:
            list_const_centroid[i] -= 1
    list_centroids = pd.DataFrame(list_centroids.drop(index=[centroid2]))
    list_centroids.reset_index(drop=True, inplace=True)
    return list_centroids

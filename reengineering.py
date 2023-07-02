import k_means
import graph
import smallStep
import transmission_lines
import matplotlib.pyplot as plt
import pandas as pd
import copy
import time


# draw centroids and points
def draw_clustering(number_figure, list_points, list_clusters, list_point_cluster=None, list_transmission_line=None):
    # print(list_clusters)
    n = list_clusters.index.size
    m = list_points.index.size
    plt.figure(number_figure)
    for i in range(n):
        for j in range(m):
            if list_point_cluster[i][j] == i:
                plt.plot([list_points.at[j, 'X'], list_clusters.at[i, 'X']],
                         [list_points.at[j, 'Y'], list_clusters.at[i, 'Y']], 'y',
                         linewidth=1, zorder=0)
    for i in range(len(list_transmission_line)):
        plt.plot([list_transmission_line[i][0], list_transmission_line[i][2]],
                 [list_transmission_line[i][1], list_transmission_line[i][3]], color="b", linewidth=2,
                 zorder=0)
    plt.scatter(list_points['X'], list_points['Y'], c='red', s=20, zorder=1)
    plt.scatter(list_clusters['X'], list_clusters['Y'], c='green', s=30, marker=(5, 2), zorder=1)


def get_centroids(n_method, list_points, n_figure=None, n_centroids=None):
    list_centroids = pd.DataFrame()
    if n_method == 1:
        # get centroids by random generation
        k_means.centroids_generation(n_centroid, 0, 5, 0, 5)
        list_centroids = pd.read_excel('Data/centroids.xlsx', index_col=0)
    elif n_method == 2:
        # get centroids from existing network
        list_centroids = pd.read_excel('Data/Coordinate_TP.xlsx', index_col=None)
    elif n_method == 3:
        # get centroids by minimal spanning tree
        weight = k_means.calculate_distance_points(list_points)
        list_centroids = graph.minimal_spanning_tree_clustering(n_figures + 1, weight, list_points)
    elif n_method == 4:
        # get centroids by minimal spanning tree
        list_centroids = smallStep.small_step(list_points, max_distances, n_figure)
    return list_centroids


def find_list(list_for_find, list_find):
    for i in range(len(list_for_find)):
        if list_for_find[i][0] == list_find[0] and list_for_find[i][1] == list_find[1] and \
                list_for_find[i][2] == list_find[2] and list_for_find[i][3] == list_find[3]:
            return True
    return False


# maximum permissible distance from point to centroid
max_distances = 1
n_points = 150
n_centroid = n_points * 0.2
n_figures = 1
n_method = 1
# 1 random 1988.2691 t1 7.5680704 t2 48.213215
# 2 existing 2020.5568 t1 0.1340167 t2 85.223714
# 3 minimum spanning tree 1847.6158 t1 7.7924799 t2 88.498879
# 4 small step 1803.4271 t1 796.62393 t2 15.494859
# fixed centroid coordinates

# random generation points for clustering
# k_means.points_generation(n_points, 0, 10, 0, 10)
# list_centroids = pd.DataFrame(columns=['X','Y'])
# k_means.centroids_generation(n_centroid, 0, 10, 0, 10)
# centroids = pd.read_excel('Data/centroids.xlsx', index_col=0)
# print(centroids)

# points coordinate in existing network
points = pd.read_excel('Data/points.xlsx', index_col=0)
n_points = points.index.size
n_centroid = int(n_points * 0.2)
n_figures = 1
plt.scatter(points['X'], points['Y'], c='red', s=20, zorder=1)
# plt.scatter(centroids['X'], centroids['Y'], c='green', s=20, zorder=1)
n_figures += 1
existing_clusters = copy.deepcopy(pd.read_excel('Data/Coordinate_TP.xlsx', index_col=None))
# print(existing_clusters)
index_const_existing_centroids = []
index_const_starting_centroids = []

plt.figure(n_figures)
# calculate distances for existing network
distances = k_means.calculate_distance(points, existing_clusters)
point_cluster = [[-1] * n_points for i in range(existing_clusters.index.size)]
existing_point_cluster = k_means.cluster_distribution(distances, -1, existing_clusters.index.size, n_points)
plt.title("start_data")

# get transmission lines
# trans_line = transmission_lines.create_transmission_line()
# transmission_line = pd.DataFrame(columns=['X1', 'Y1', 'X2', 'Y2'])
# transmission_line.loc[0] = {'X1': trans_line[0],'Y1': trans_line[1], 'X2': trans_line[2],'Y2': trans_line[3]}
# transmission_line.to_csv("Data/Transmission_line.csv", index=None)
transmission_line = pd.read_csv("Data/Transmission_line.csv", index_col=None)
transmission_line = transmission_line.values.tolist()
existing_list_line = transmission_lines.get_transmission_lines(transmission_line, existing_clusters)
draw_clustering(n_figures, points, existing_clusters, point_cluster, existing_list_line)

len_line = 0
c_line = 100
c_new_TP = 10000
c_modern_TP = 1000
c_transmission_line = 500
total_c = 0
for i in range(existing_clusters.index.size):
    for j in range(n_points):
        if existing_point_cluster[i][j] == i:
            len_line += k_means.evclid_distance(existing_clusters.at[i, 'X'], existing_clusters.at[i, 'Y'],
                                                points.at[i, 'X'], points.at[i, 'Y']) * c_line
total_c += len_line
print(total_c)

n_figures += 1
k = 0
set_centroid = [0 for i in range(4)]
clustering = [0 for i in range(4)]
total_value = [0 for i in range(4)]

while k < 1:
    n_method = 4
    while n_method < 5:
        start_time = time.time()
        if n_method == 4:
            start_centroids = get_centroids(n_method, points, n_figures)
            n_figures += 1
        if n_method == 1:
            start_centroids = get_centroids(n_method, points, n_centroids=n_centroid)
        else:
            start_centroids = get_centroids(n_method, points)
        end_time = time.time()
        print(n_method)
        set_centroid[n_method - 1] = end_time - start_time
        print("set centroids %s" % (end_time - start_time))
        centroids = copy.deepcopy(start_centroids)
        n_centroid = centroids.index.size
        old_point_cluster = [[-1] * n_points for i in range(n_centroid)]
        old_list_centroids = copy.deepcopy(centroids)
        is_add_centroid = False
        is_delete_centroid = False
        is_finish = False

        start_time = time.time()
        while True:
            const_cluster = copy.deepcopy(index_const_starting_centroids)
            old_const_cluster = copy.deepcopy(index_const_starting_centroids)
            while True:
                # k_means
                while True:
                    distances = k_means.calculate_distance(points, centroids)
                    point_cluster = k_means.cluster_distribution(distances, max_distances, n_centroid, n_points)
                    if k_means.compare_array(point_cluster, old_point_cluster, n_centroid, n_points):
                        break
                    k_means.recalculation_centroids(points, point_cluster, centroids, const_cluster)
                    old_point_cluster = point_cluster

                index_point_outside = k_means.find_index_outside_point(point_cluster, n_centroid, n_points)
                # termination condition
                if is_finish or (-1 == index_point_outside and is_add_centroid):
                    # n_figures += 1
                    # list_line = transmission_lines.get_transmission_lines(transmission_line, centroids)
                    # draw_clustering(n_figures, points, centroids, point_cluster, list_line)
                    break

                # adding centroids
                if index_point_outside != -1 and not is_delete_centroid:
                    is_add_centroid = True
                    centroids.loc[n_centroid] = {'X': points.at[index_point_outside, 'X'],
                                                 'Y': points.at[index_point_outside, 'Y']}
                    old_point_cluster = [[-1] * n_points for i in range(n_centroid)]
                    n_centroid = n_centroid + 1

                # drop centroids
                if not is_add_centroid and not is_finish:
                    if -1 == index_point_outside:
                        is_delete_centroid = True
                        distances_between_centroids = k_means.calculate_distance_centroids(centroids)
                        while True:
                            i, j = k_means.min_distance(distances_between_centroids, n_centroid, n_centroid)
                            if transmission_lines.find_element_in_list(j, const_cluster) is not None or \
                                    transmission_lines.find_element_in_list(i, const_cluster) is not None:
                                distances_between_centroids[i][j] = -1
                                distances_between_centroids[j][i] = -1
                            else:
                                break
                        if i != -1 or j != -1:
                            old_list_centroids = copy.deepcopy(centroids)
                            old_const_cluster = copy.deepcopy(const_cluster)
                            centroids = k_means.delete_centroid(centroids, i, j, const_cluster)
                            n_centroid = n_centroid - 1
                            old_point_cluster = [[-1] * n_points for i in range(n_centroid)]
                        else:
                            is_finish = True
                            break
                    else:
                        centroids = copy.deepcopy(old_list_centroids)
                        const_cluster = copy.deepcopy(old_const_cluster)
                        n_centroid = n_centroid + 1
                        is_finish = True

            # size old_centroids - number columns, size new_list - number rows
            distance_centroids = k_means.calculate_distance(existing_clusters, centroids)
            n = centroids.index.size
            m = existing_clusters.index.size
            while True:
                min_i, min_j = k_means.min_distance(distance_centroids, n, m)
                if transmission_lines.find_element_in_list(min_j, index_const_existing_centroids) is not None:
                    distance_centroids[min_i][min_j] = -1
                else:
                    break
            if distance_centroids[min_i][min_j] <= max_distances / 10 and distance_centroids[min_i][min_j] != -1:
                dist = []
                for i in range(start_centroids.index.size):
                    dist.append(
                        k_means.evclid_distance(existing_clusters.at[min_j, 'X'], existing_clusters.at[min_j, 'Y'],
                                                start_centroids.at[i, 'X'], start_centroids.at[i, 'Y']))
                min_d = -1
                index = -1
                for i in range(start_centroids.index.size):
                    if min_d > dist[i] >= 0 or min_d == -1 and dist[i] >= 0 and \
                            transmission_lines.find_element_in_list(i, index_const_starting_centroids) is None:
                        min_d = dist[i]
                        index = i

                start_centroids.at[index, 'X'] = existing_clusters.at[min_j, 'X']
                start_centroids.at[index, 'Y'] = existing_clusters.at[min_j, 'Y']
                index_const_existing_centroids.append(min_j)
                index_const_starting_centroids.append(index)
                centroids = copy.deepcopy(start_centroids)
                old_list_centroids = copy.deepcopy(centroids)
                n_centroid = centroids.index.size
                is_add_centroid = False
                is_delete_centroid = False
                is_finish = False
                old_point_cluster = [[-1] * n_points for i in range(n_centroid)]

            else:
                # print(centroids)
                # print(index_const_existing_centroids)
                # print(index_const_starting_centroids)
                # print(const_cluster)
                list_line = transmission_lines.get_transmission_lines(transmission_line, centroids)

                draw_clustering(n_figures, points, centroids, point_cluster, list_line)
                plt.title(n_method)
                n_figures += 1

                break
        end_time = time.time()
        clustering[n_method - 1] = end_time - start_time
        print("clustering %s" % (end_time - start_time))
        len_line = 0
        c_line = 100
        c_new_TP = 10000
        c_modern_TP = 1000
        c_transmission_line = 500
        total_c = 0
        for i in range(n_centroid):
            for j in range(n_points):
                if point_cluster[i][j] == i:
                    if transmission_lines.find_element_in_list(i, const_cluster) is not None:
                        index = index_const_existing_centroids[
                            transmission_lines.find_element_in_list(i, const_cluster)]
                        if existing_point_cluster[index][j] == index:
                            continue
                    else:
                        len_line += k_means.evclid_distance(centroids.at[i, 'X'], centroids.at[i, 'Y'],
                                                            points.at[i, 'X'], points.at[i, 'Y']) * c_line
        total_c += len_line
        print(len_line)
        total_c += (centroids.index.size - len(const_cluster)) * c_new_TP
        total_c += len(const_cluster) * c_modern_TP
        sum_transmission_line = 0
        for i in range(len(list_line)):
            if find_list(existing_list_line, list_line[i]):
                continue
            sum_transmission_line += k_means.evclid_distance(list_line[i][0], list_line[i][1],
                                                             list_line[i][2], list_line[i][3]) * c_transmission_line
        total_c += sum_transmission_line
        total_value[n_method - 1] = total_c
        print(total_c)
        n_method += 1
        index_const_existing_centroids = []
        index_const_starting_centroids = []
    k += 1
    print(k)
for i in range(4):
    set_centroid[i] = set_centroid[i] / k
    clustering[i] = clustering[i] / k
    total_value[i] = total_value[i] / k
print(set_centroid)
print(clustering)
print(total_value)
plt.show()

import math
import random
import k_means
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import lines, pylab


def create_transmission_line():
    coordinate = [0, random.uniform(0, 3), 5, random.uniform(2, 5)]
    return coordinate


def min_distance(list_distance, n):
    min_d = -1
    index = -1
    for i in range(n):
        if min_d > list_distance[i] > 0 or min_d == -1 and list_distance[i] > 0:
            min_d = list_distance[i]
            index = i
    return min_d, index


def intersection_point(a1, b1, c1, a2, b2, c2):
    d = b2 * a1 - b1 * a2
    if d != 0:
        x = (c1 * b2 - b1 * c2) / d
        y = (a1 * c2 - c1 * a2) / d

    return x, y


def distance_point_line(list_centroids, a, b, c):
    point_line = pd.DataFrame(columns=['i', 'X', 'Y', 'distance'])
    for i in range(list_centroids.index.size):
        a_i = b
        b_i = -a
        c_i = b * list_centroids.at[i, 'X'] - a * list_centroids.at[i, 'Y']
        x, y = intersection_point(a, b, c, a_i, b_i, c_i)
        d = k_means.evclid_distance(x, y, list_centroids.at[i, 'X'], list_centroids.at[i, 'Y'])
        point_line.loc[i] = {'i': i, 'X': x, 'Y': y, 'distance': d}
        point_line = point_line.sort_values('distance')
    return point_line


def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return None


def get_transmission_lines(transmission_line, centroids):
    a = transmission_line[0][1] - transmission_line[0][3]
    b = transmission_line[0][2] - transmission_line[0][0]
    c = transmission_line[0][0] * transmission_line[0][3] + transmission_line[0][2] * transmission_line[0][1]
    list_lines = []
    list_index_coordinate = []
    point_to_line = distance_point_line(centroids, a, b, c)
    ind = int(point_to_line.at[0, 'i'])
    list_lines.append(list([point_to_line.at[0, 'X'], point_to_line.at[0, 'Y'],
                            centroids.at[ind, 'X'], centroids.at[ind, 'Y']]))
    list_index_coordinate.append(ind)
    distance = k_means.calculate_distance_centroids(centroids)
    for i in range(1, point_to_line.index.size):
        number_point = int(point_to_line.at[i, 'i'])
        d, index = min_distance(distance[number_point], centroids.index.size)
        if point_to_line.at[i, 'distance'] > d and find_element_in_list(
                index, list_index_coordinate) is not None:
            list_lines.append(list([centroids.at[number_point, 'X'], centroids.at[number_point, 'Y'],
                                    centroids.at[index, 'X'], centroids.at[index, 'Y']]))
            list_index_coordinate.append(number_point)
        else:
            list_lines.append(list([point_to_line.at[i, 'X'], point_to_line.at[i, 'Y'],
                                    centroids.at[number_point, 'X'],
                                    centroids.at[number_point, 'Y']]))
            list_index_coordinate.append(number_point)

    # list_lines.append(
    #     list([centroids.at[index, 'X'], centroids.at[index, 'Y'], centroids.at[i, 'X'], centroids.at[i, 'Y']]))
    list_lines.append(list([transmission_line[0][0], transmission_line[0][1], transmission_line[0][2],
                            transmission_line[0][3]]))
    print(list_lines)
    return list_lines

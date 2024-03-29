# -*- coding: utf-8 -*-
"""
===================================
Demo of DBSCAN clustering algorithm
===================================

Finds core samples of high density and expands clusters from them.

"""
print(__doc__)

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import os
import pandas as pd



##############################################################################
# Generate sample data
# centers = [[1, 1], [-1, -1], [1, -1]]
# X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
#                             random_state=0)

# print labels_true
# print X

dataDir = os.path.join(os.path.dirname(os.path.abspath('')), 'data')

data = pd.read_csv(os.path.join(dataDir, 'Storm_Anomalies.csv'))

print(data.shape)
# kmeans_model = KMeans(n_clusters=5, random_state=1)
# good_columns = data._get_numeric_data()


X = StandardScaler().fit_transform(data)
# print X
##############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.9, min_samples=40).fit(X)
# core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
#
# core_samples_mask[db.core_sample_indices_] = True

print(type(db))
print(db.leaf_size)
print(db.algorithm)

print(db.eps)

print(db.min_samples)
print(db.n_jobs)
labels = db.labels_

print(type(labels))
# print X[labels == -1]
# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print(('Estimated number of clusters: %d' % n_clusters_))

data['Target'] = labels

print(data)
data2 = data[data["Target"] != -1]
data.to_csv(os.path.join(dataDir, 'pyStorm_anomaly.csv'))
data2.to_csv(os.path.join(dataDir, 'pyStorm_anomaly2.csv'))
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# print("Adjusted Rand Index: %0.3f"
#       % metrics.adjusted_rand_score(labels_true, labels))
# print("Adjusted Mutual Information: %0.3f"
#       % metrics.adjusted_mutual_info_score(labels_true, labels))
# print("Silhouette Coefficient: %0.3f"
#       % metrics.silhouette_score(X, labels))

# ##############################################################################
# # Plot result
# import matplotlib.pyplot as plt
#
# # Black removed and is used for noise instead.
# unique_labels = set(labels)
# colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         # Black used for noise.
#         col = 'k'
#
#     class_member_mask = (labels == k)
#
#     xy = X[class_member_mask & core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#              markeredgecolor='k', markersize=14)
#
#     xy = X[class_member_mask & ~core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#              markeredgecolor='k', markersize=6)
#
# plt.title('Estimated number of clusters: %d' % n_clusters_)
# plt.show()

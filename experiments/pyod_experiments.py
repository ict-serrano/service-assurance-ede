


import os
import sys
import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.font_manager

# Import all models
from pyod.models.abod import ABOD
from pyod.models.cblof import CBLOF
from pyod.models.feature_bagging import FeatureBagging
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.mcd import MCD
from pyod.models.ocsvm import OCSVM
from pyod.models.pca import PCA
from time import time

# temporary solution for relative imports in case pyod is not installed
# if pyod is installed, no need to use the following line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))


# Experimental data directory
dataDir = '/Users/Gabriel/Documents/workspaces/diceWorkspace/dmon-adp/data'
data = os.path.join(dataDir, 'CEP_Complete_Labeled_Extended.csv')

df = pd.read_csv(data)
df.set_index('key', inplace=True)
dropList = ['host', 'ship', 'method']
print("Droped columns are: %s" % dropList)
df = df.drop(dropList, axis=1)
print("Index Name: %s" % df.index.name)

# encode dataframe
col = []
for el, v in df.dtypes.items():
    # print el
    if v == 'object':
        col.append(el)


def ohEncoding(data, cols, replace=False):
    vec = DictVectorizer()
    mkdict = lambda row: dict((col, row[col]) for col in cols)
    vecData = pd.DataFrame(vec.fit_transform(data[cols].apply(mkdict, axis=1)).toarray())
    vecData.columns = vec.get_feature_names()
    vecData.index = data.index
    if replace is True:
        data = data.drop(cols, axis=1)
        data = data.join(vecData)
    return data, vecData, vec


df, t, v = ohEncoding(df, col, replace=True)

print("Shape after encoding")
print(type(df.shape))

df_unlabeled = df.drop("Anomaly", axis=1)
print ("Shape of the dataframe without anomaly column: ")
print (df_unlabeled.shape)



# Define the number of inliers and outliers
n_samples = 200
outliers_fraction = 0.25
clusters_separation = [0]

# Compare given detectors under given settings
# Initialize the data
xx, yy = np.meshgrid(np.linspace(-7, 7, 100), np.linspace(-7, 7, 100))
n_inliers = int((1. - outliers_fraction) * n_samples)
n_outliers = int(outliers_fraction * n_samples)
ground_truth = np.zeros(n_samples, dtype=int)
ground_truth[-n_outliers:] = 1

# Show the statics of the data
print('Number of inliers: %i' % n_inliers)
print('Number of outliers: %i' % n_outliers)
print('Ground truth shape is {shape}. Outlier are 1 and inliers are 0.\n'.format(shape=ground_truth.shape))
print(ground_truth)

# print(type(xx))
# print(xx)
print(yy.shape)
sys.exit()



random_state = np.random.RandomState(42)
# Define nine outlier detection tools to be compared
classifiers = {'Angle-based Outlier Detector (ABOD)':
                   ABOD(n_neighbors=10,
                        contamination=outliers_fraction),
               'Cluster-based Local Outlier Factor (CBLOF)':
                   CBLOF(contamination=outliers_fraction,
                         check_estimator=False, random_state=random_state),
               'Feature Bagging':
                   FeatureBagging(LOF(n_neighbors=35),
                                  contamination=outliers_fraction,
                                  check_estimator=False,
                                  random_state=random_state),
               'Histogram-base Outlier Detection (HBOS)': HBOS(
                   contamination=outliers_fraction),
               'Isolation Forest': IForest(contamination=outliers_fraction,
                                           random_state=random_state),
               'K Nearest Neighbors (KNN)': KNN(
                   contamination=outliers_fraction),
               'Average KNN': KNN(method='mean',
                                  contamination=outliers_fraction),
               'Median KNN': KNN(method='median',
                                 contamination=outliers_fraction),
               'Local Outlier Factor (LOF)':
                   LOF(n_neighbors=35, contamination=outliers_fraction),
               'Minimum Covariance Determinant (MCD)': MCD(
                   contamination=outliers_fraction, random_state=random_state),
               'One-class SVM (OCSVM)': OCSVM(contamination=outliers_fraction,
                                              random_state=random_state),
               'Principal Component Analysis (PCA)': PCA(
                   contamination=outliers_fraction, random_state=random_state),
               }

# Show all detectors
for i, clf in enumerate(classifiers.keys()):
    print('Model', i + 1, clf)

# Fit the models with the generated data and
# compare model performances
for i, offset in enumerate(clusters_separation):
    np.random.seed(42)
    # Data generation
    X1 = 0.3 * np.random.randn(n_inliers // 2, 2) - offset
    X2 = 0.3 * np.random.randn(n_inliers // 2, 2) + offset
    X = np.r_[X1, X2]
    # Add outliers
    X = np.r_[X, np.random.uniform(low=-6, high=6, size=(n_outliers, 2))]

    # Fit the model
    plt.figure(figsize=(15, 12))
    for i, (clf_name, clf) in enumerate(classifiers.items()):
        print(i + 1, 'fitting', clf_name)
        # fit the data and tag outliers
        clf.fit(X)
        scores_pred = clf.decision_function(X) * -1
        y_pred = clf.predict(X)
        threshold = stats.scoreatpercentile(scores_pred,
                                            100 * outliers_fraction)
        n_errors = (y_pred != ground_truth).sum()
        # plot the levels lines and the points

        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]) * -1
        Z = Z.reshape(xx.shape)
        subplot = plt.subplot(3, 4, i + 1)
        subplot.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7),
                         cmap=plt.cm.Blues_r)
        a = subplot.contour(xx, yy, Z, levels=[threshold],
                            linewidths=2, colors='red')
        subplot.contourf(xx, yy, Z, levels=[threshold, Z.max()],
                         colors='orange')
        b = subplot.scatter(X[:-n_outliers, 0], X[:-n_outliers, 1], c='white',
                            s=20, edgecolor='k')
        c = subplot.scatter(X[-n_outliers:, 0], X[-n_outliers:, 1], c='black',
                            s=20, edgecolor='k')
        subplot.axis('tight')
        subplot.legend(
            [a.collections[0], b, c],
            ['learned decision function', 'true inliers', 'true outliers'],
            prop=matplotlib.font_manager.FontProperties(size=10),
            loc='lower right')
        subplot.set_xlabel("%d. %s (errors: %d)" % (i + 1, clf_name, n_errors))
        subplot.set_xlim((-7, 7))
        subplot.set_ylim((-7, 7))
    plt.subplots_adjust(0.04, 0.1, 0.96, 0.94, 0.1, 0.26)
    plt.suptitle("Outlier detection")
plt.show()

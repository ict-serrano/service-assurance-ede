"""
Copyright 2021, Institute e-Austria, Timisoara, Romania
    http://www.ieat.ro/
Developers:
 * Gabriel Iuhasz, iuhasz.gabriel@info.uvt.ro

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt
from yellowbrick.features import Rank2D, Rank1D, Manifold
from yellowbrick.features import PCA
from sklearn import preprocessing




def user_iso(n_estimators,
             contamination,
             max_features,
             n_jobs,
             warm_start,
             random_state,
             bootstrap,
             verbose,
             max_samples):
    '''
    Example of user defined unsupervised predictive model
    :param behaviour:
    :param n_estimators:
    :param contamination:
    :param max_features:
    :param n_jobs:
    :param warm_start:
    :param random_state:
    :param bootstrap:
    :param verbose:
    :param max_samples:
    :return: model instance
    '''
    clf = IsolationForest(
        n_estimators=n_estimators,
             contamination=contamination,
             max_features=max_features,
             n_jobs=n_jobs,
             warm_start=warm_start,
             random_state=random_state,
             bootstrap=bootstrap,
             verbose=verbose,
             max_samples=max_samples)
    return clf


def wrapper_add_columns(columns=(None, None),
                        column_name=None):
    '''
    Wrapper function example which wraps user defined
    feature engineering function
    :param columns:
    :param column_name:
    :return:
    '''
    def add_columns(df,
                    columns=columns,
                    column_name=column_name):
        if columns[0] is None:
            return df
        sum_col = df[columns[0]]+df[columns[1]]
        df[column_name] = sum_col
        return df
    return add_columns


def wrapper_analysis_corr(name,
                     annot=True,
                     cmap='RdBu_r',
                     columns=[],
                     location=None):
    def pearson_corelation_heatmap(data,
                                   name=name,
                                   annot=annot,
                                   cmap=cmap,
                                   columns=columns,
                                   location=location):
        data = data[columns]
        # data = data.set_index('time', inplace=False)
        data = data.astype(float)
        # print(data.shape)
        # print(data.dtypes)
        corr = data.corr(method='pearson')
        # print(corr.shape)
        plt.subplots(figsize=(20, 15))
        sns_plot = sns.heatmap(corr,
                               xticklabels=corr.columns,
                               yticklabels=corr.columns,
                               annot=annot,
                               cmap=cmap)
        fig = sns_plot.get_figure()
        fig_loc = os.path.join(location, "pearson_corr_{}.png".format(name))
        file_loc = os.path.join(location, "pearson_corr_{}.csv".format(name))
        corr.to_csv(file_loc)
        fig.savefig(fig_loc, bbox_inches="tight")
        plt.close()
        return name
    return pearson_corelation_heatmap


def wrapper_analysis_plot(name,
                          columns,
                          location):
    def line_plot(data,
                  name=name,
                  columns=columns,
                  location=location):
        data = data.astype(float)
        sns_plot = sns.lineplot(
            x='time',
            y='node_load1_10.211.55.101:9100',
            data=data[columns]
        )
        # sns_plot = sns.replot(x=)
        fig = sns_plot.get_figure()
        fig_loc = os.path.join(location, "lineplot_{}.png".format(name))
        fig.savefig(fig_loc, bbox_inches="tight")
        plt.close()
        return name
    return line_plot


def wrapper_rank1(name,
                  location,
                  dcol=[],
                  algorithm='shapiro',
                  ):
    """
    Compute and generate heatmap for different feature ranking 1D methods including:
    shapiro
    :param name: name to be used for visualization
    :param location: location to save the heatmap
    :param dcol: columns to be droped
    :param algorithm: select the ranking algorithm to be used
    :return:
    """
    def rank1(data,
              name=name,
              location=location,
              dcol=dcol,
              algorithm=algorithm):
        df_data = data.drop(dcol, axis=1)
        df_data = df_data.astype(float)
        ax = plt.axes()
        visualizer = Rank1D(algorithm=algorithm, size=(1200, 1200), ax=ax)
        visualizer.fit(df_data)  # Fit the data to the visualizer
        visualizer.transform(df_data)
        visualizer.show(outpath=os.path.join(location, f"Rank1D_{algorithm}_{name}_unsorted.png"))
        plt.close()
        # Add to dataframe for custom visualization
        df_rank1d = pd.DataFrame()
        df_rank1d['features'] = visualizer.features_
        df_rank1d['rank'] = visualizer.ranks_
        # df_anomaly_rank1d.set_index('rank', inplace=True)
        df_rank1d.sort_values(by=['rank'], inplace=True, ascending=False)  # Sort by rank decesnding
        df_rank1d.plot(kind='bar', x="features", rot=1, title=f"{algorithm} rank", sort_columns=True, figsize=(30,45))
        df_rank1d.to_csv(os.path.join(location, f"Rank1D_{algorithm}_{name}.csv"), index=False)
        plt.xticks(rotation=90)
        plt.savefig(os.path.join(location, f"Rank1D_{algorithm}_{name}.png"), bbox_inches="tight")#
        plt.close()
        return name
    return rank1

def wrapper_rank2(name,
                          location,
                          dcol=[],
                          algorithm='pearson',
                          colormap = 'RdBu_r',
                          show=False):
    """
    Compute and generate heatmap for different feature ranking methods including:
    'pearson’, ‘covariance’, ‘spearman’, or ‘kendalltau'
    :param name: name to be used for visualization
    :param location: location to save the heatmap
    :param dcol: columns to be droped
    :param algorithm: select the ranking algorithm to be used
    :param colormap: colormap to be used for vizualization
    :param show: if True feature names will be added
    :return:
    """
    def rank2(data,
                      name=name,
                      location=location,
                      dcol=dcol,
                      algorithm=algorithm,
                      colormap=colormap,
                      show=show):
        df_data = data.drop(dcol, axis=1)
        df_data = df_data.astype(float)
        ax = plt.axes()
        rk2d2 = Rank2D(ax=ax, algorithm=algorithm, show_feature_names=show, size=(1080, 720), colormap=colormap)
        ax.set_title(name)
        rk2d2.fit(df_data)
        rk2d2.transform(df_data)
        rk2d2.show(outpath=os.path.join(location, f"Correlation_{algorithm}_{name}.png"))
        plt.close()
        return name
    return rank2


def wrapper_improved_pearson(name,
                             location,
                             dcol=[],
                             cmap='coolwarm',
                             show=False):
    """
    Computes the Pearson correlation between features. If the augmentation step is
    not used and categorical features are still present these will be converted from object dtypes
    to float.
    :param name: name to be used for visualization
    :param location: location to save the heatmap
    :param dcol: columns to be droped
    :param cmap: color map
    :param show: show feature names
    :return: name
    """

    def improved_pearsons(data,
                         name=name,
                         location=location,
                         dcol=dcol,
                         cmap=cmap,
                         show=show):

        # Detect object columns and convert them to float
        df_data = data.drop(dcol, axis=1)
        df_data = df_data.astype(float)
        # Compute pearson corelation
        p_test = df_data.corr()
        # Generate mask for upper half
        mask = np.triu(np.ones_like(p_test, dtype=bool))

        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(25, 15))

        # Custom color map
        # cmap = sns.diverging_palette(230, 20, as_cmap=True)
        # ax = plt.axes()

        ht_hm = sns.heatmap(p_test, mask=mask, ax=ax, cmap=cmap, annot=show)
        ax.set_title(f'Person correlation {name}', fontsize=20)
        hm_fig = "Pearson_{}.png".format(name)
        ht_hm.figure.savefig(os.path.join(location, hm_fig), bbox_inches="tight")
        plt.close()
        return name
    return improved_pearsons


def wrapper_pca_plot(name,
                     location,
                     target='target',
                     projection=2):
    """
    Creates a PCA plot based on the available target data using a
    2 or 3D projection.
    :param name: name to be used for visualization
    :param location: location to save the figure
    :param target: target (ground truth) column name, if mising this plot will be skipped
    :param projection: 2 or 3 Dimenisonal projection
    :return:
    """
    def pca_plot(data,
                 location=location,
                 name=name,
                 projection=projection,
                 target=target):
        classes = data[target].unique()
        data[target].replace(0, "0", inplace=True)
        le = preprocessing.LabelEncoder()
        le.fit(data[target])
        y = le.transform(data[target])
        data_test = data.drop([target], axis=1)
        ax = plt.axes()
        visualizer = PCA(
            scale=True,
            projection=projection,
            classes=classes,
            title=f"Principle component Plot {name}",
        )
        visualizer.fit_transform(data_test, y)
        plot_name = f"PrincipalComponent_Projection_{projection}_{name}.png"
        visualizer.show(outpath=os.path.join(location, plot_name))
        plt.close()
        return 0
    return pca_plot


def wrapper_manifold(name,
                     location,
                     target='target',
                     manifold='tsne',
                     n_neighbors=10
                     ):
    """
    The Manifold visualizer provides high dimensional visualization using manifold learning
    to embed instances described by many dimensions into 2, thus allowing the creation of
    a scatter plot that shows latent structures in data. Currently supported methods are those from
    supported by scikit-learn:

    "lle" Locally Linear Embedding (LLE) uses many local linear decompositions to preserve globally non-linear structures.
    "ltsa" LTSA LLE: local tangent space alignment is similar to LLE in that it uses locality to preserve neighborhood distances.
    "hessian" Hessian LLE an LLE regularization method that applies a hessian-based quadratic form at each neighborhood
    "modified" Modified LLE applies a regularization parameter to LLE.
    "isomap" Isomap seeks a lower dimensional embedding that maintains geometric distances between each instance.
    "mds" MDS: multi-dimensional scaling uses similarity to plot points that are near to each other close in the embedding.
    "spectral" Spectral Embedding a discrete approximation of the low dimensional manifold using a graph representation.
    "tsne" t-SNE: converts the similarity of points into probabilities then uses those probabilities to create an embedding.

    :param name: name to be used for visualization
    :param location: location to save the figure
    :param target: target (ground truth) column name, if missing this plot will be skipped unless default value is found
    :param manifold: manifold empeding method to be used
    :param n_neighbors: number of nearest neighbours, some methods might not use it
    :return: 0
    """
    def manifold_embeding(data,
                 name=name,
                 location=location,
                 target=target,
                 manifold=manifold,
                 n_neighbors=n_neighbors):

        classes = data[target].unique()
        data[target].replace(0, "0", inplace=True)
        le = preprocessing.LabelEncoder()
        le.fit(data[target])
        y = le.transform(data[target])
        data_test = data.drop([target], axis=1)
        ax = plt.axes()
        vizualisation = Manifold(classes=classes, manifold=manifold, n_neighbors=n_neighbors, ax=ax)
        vizualisation.fit_transform(data_test, y)
        plot_name = f"Manifold_{manifold}_{name}.png"
        vizualisation.show(outpath=os.path.join(location, plot_name))
        plt.close()

    return manifold_embeding


def wrapper_plot_on_features(name,
                             location,
                             target='target',
                             features=[]):
    def plot_on_features(data,
                         name=name,
                         location=location,
                         target=target,
                         features=features,
                         ):
        """
        :param data: dataset used for training or prediction
        :param name: name to be used for visualization
        :param location: location to save the figure
        :param target: target (ground truth) column name, if missing this plot will be skipped unless default value is found
        :param features: features to be ploted
        :return: 0
        """
        if not features:
            col_names_plt = list(data.columns.values)
        else:
            col_names_plt = features

        for feature in col_names_plt:
            if feature == 'time' or feature == target:
                pass
            else:
                # fig, ax = plt.subplots(figsize=(15,10))
                a = data[data[target] == 'target_cpu_master'] #class
                b = data[data[target] == 'target_mem_master'] #class
                c = data[data[target] == 'target_copy_master'] #class
                d = data[data[target] == 'target_ddot_master'] #class
                _ = plt.figure(figsize=(15,5))
                _ = plt.plot(data[feature], color='blue', label='Normal')
                _ = plt.plot(a[feature], linestyle='none', marker='X', color='red', markersize=4, label='CPU')
                _ = plt.plot(b[feature], linestyle='none', marker='o', color='green', markersize=4, label='MEM')
                _ = plt.plot(c[feature], linestyle='none', marker='*', color='m', markersize=4, label='COPY')
                _ = plt.plot(d[feature], linestyle='none', marker='.', color='y', markersize=4, label='DDOT')
                _ = plt.xlabel('Time')
                _ = plt.ylabel(f'{feature}')
                _ = plt.title(f'Anomaly Classes for {feature}')
                _ = plt.grid()
                _ = plt.legend(loc='best')
                plot_name = f"Feature_plot_{feature}_{name}.png"
                plt.savefig(os.path.join(location, plot_name), bbox_inches="tight")
                plt.close();
        return 0
    return plot_on_features

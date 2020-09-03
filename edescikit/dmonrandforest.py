from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import numpy as np
import glob


dataDir = os.path.join(os.path.dirname(os.path.abspath('')), 'data')
modelDir = os.path.join(os.path.dirname(os.path.abspath('')), 'models')

data = pd.read_csv(os.path.join(dataDir, 'Storm_anomalies_Clustered.csv'))
data.set_index('key', inplace=True)
import pickle as pickle

#drop missing values
data = data.dropna()

# View the top 5 rows
# print data.head

# Create a list of the feature column's names, last one is always the target

# df = df.drop('column_name', 1)
features = data.columns[:-1]


print(type(features))
for f in features:
    if f == "Winner_Cluster":
        print("FOUND")

# train['species'] contains the actual species names. Before we can use it,
# we need to convert each species name into a digit. So, in this case there
# are three species, which have been coded as 0, 1, or 2.

# Might need this for ADT!!! TODO
# y = pd.factorize(train['species'])[0]
# print y
X = data[features]

y = data['TargetF'].values
print("%^&*100")
# print y

# Target always last column of dataframe
y2 = data.iloc[:,-1].values
print(y2)

method = 'randomforest'
mname = 'testoffline'

# Create a random forest classifier. By convention, clf means 'classifier'
clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1, n_jobs=-1)
clf.fit(data[features], y)

# Apply the classifier we trained to the test data (which, remember, it has never seen before)
predict = clf.predict(data[features])
# print predict

# View the predicted probabilities of the first 10 observations
predProb = clf.predict_proba(data[features])
# print predProb

score = clf.score(data[features], y)
print(score)

# # Create confusion matrix
# print pd.crosstab(test['species'], preds, rownames=['Actual Species'], colnames=['Predicted Species'])
#
# View a list of the features and their importance scores
print(list(zip(data[features], clf.feature_importances_)))

method = 'randomforest'
mname = 'testoffline'

fpath = "%s_%s.pkl" % ('randomforest', mname)
fname = os.path.join(modelDir, fpath)
pickle.dump(clf, open(fname, "wb"))
print('Saved %s model at %s' % (method, fpath))


def __loadClassificationModel(method, model):
    '''
    :param method: -> method name
    :param model: -> model name
    :return: -> instance of serialized object
    '''
    lmodel = glob.glob(os.path.join(modelDir, ("%s_%s.pkl" % (method, model))))
    if not lmodel:
        print("No %s model with the name %s found" % (method, model))
        return 0
    else:
        smodel = pickle.load(open(lmodel[0], "rb"))
        print("Succesfully loaded %s model with the name %s" % (method, model))
        return smodel


loaded_classifier = __loadClassificationModel(method=method, model=mname)
print("Detected RandomForest model")
print("n_estimators -> %s" % loaded_classifier.n_estimators)
print("Criterion -> %s" % loaded_classifier.criterion)
print("Max_Features -> %s" % loaded_classifier.max_features)
print("Max_Depth -> %s" % loaded_classifier.max_depth)
print("Min_sample_split -> %s " % loaded_classifier.min_samples_split)
print("Min_sample_leaf -> %s " % loaded_classifier.min_samples_leaf)
print("Min_weight_fraction_leaf -> %s " % loaded_classifier.min_weight_fraction_leaf)
print("Max_leaf_nodes -> %s " % loaded_classifier.max_leaf_nodes)
print("Min_impurity_split -> %s " % loaded_classifier.min_impurity_split)
print("Bootstrap -> %s " % loaded_classifier.bootstrap)
print("Oob_score -> %s " % loaded_classifier.oob_score)
print("N_jobs -> %s " % loaded_classifier.n_jobs)
print("Random_state -> %s " % loaded_classifier.random_state)
print("Verbose -> %s " % loaded_classifier.verbose)
print("Class_weight -> %s " % loaded_classifier.class_weight)


dpredict = loaded_classifier.predict(X)
print("RandomForest Prediction Array -> %s" %str(dpredict))

anomalyarray = np.argwhere(dpredict != 0)

X['Target'] = dpredict

for index, row in X.iterrows():
    if row['Target'] != 0:
        print(index)
        print(X.get_value(index, 'Target'))
# print anomalyarray
# anomalieslist = []
# for an in anomalyarray:
#     # print X.iloc[an[0]]
#     print an
#     # anomalies = {}
#     # anomalies['utc'] = int(X.iloc[an[0]]['key'])

#     anomalieslist.append(anomalies)
# anomaliesDict = {}
# anomaliesDict['anomalies'] = anomalieslist
# print anomaliesDict
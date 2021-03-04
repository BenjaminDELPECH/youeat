# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import DBSCAN
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor, GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier

import pandas as pd

classifiers = [
    LogisticRegression(),
    LinearSVC(),
    KMeans(),
    MiniBatchKMeans(),
    SVC(),
    RandomForestClassifier(),
    KNeighborsClassifier(n_neighbors=4),
    GaussianNB(),
    Perceptron(),
    SGDClassifier(),
    DecisionTreeClassifier(),
    GradientBoostingClassifier(),
    AdaBoostClassifier()
]

#TODO X_train -> stringToMapCol,  Y_train -> theFinalString


foodAsociations = pd.read_csv(
    'C:\\dev\\perso\\simplenutritionfullstack\\Django\\machineLearning\\mapStrings\\test.csv', sep=';')
X_train  = []
Y_train  = []
for i, v in foodAsociations.iterrows():
    if v.nameFr and :
        X_train.append({"marmimittonFoodName": v.marmittonFoodName})
        Y_train.append({"foodName": v.nameFr})

for classifier in classifiers:
    classifier.fit(X_train, Y_train)
    predictions = classifier.predict(X_test)
    score = classifier.score(X_train, Y_train)
    print(classifier.__class__.__name__ + " : " + str(score))
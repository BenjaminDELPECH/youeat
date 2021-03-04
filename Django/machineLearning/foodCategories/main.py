# data analysis and wrangling
import pandas as pd
import numpy as np
import random as rnd

# visualization
import seaborn as sns
import matplotlib.pyplot as plt

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

# from completing import completAge
# from converting import *
# from creating import *


foods = pd.read_csv(
    'C:\\dev\\perso\\simplenutritionfullstack\\Django\\machineLearning\\foodCategories\\input\\foods_food2.csv')
lnf = pd.read_csv(
    'C:\\dev\\perso\\simplenutritionfullstack\\Django\\machineLearning\\foodCategories\\input\\nutrients_linknutrientfood.csv')

train_df = []

import math

train_df = [0 for i in range(319001)]
test_df = [0 for i in range(319001)]

food_id_list = []
for i, v in foods.iterrows():
    obj = {"foodId": v.id, "foodGroup_id": v.foodGroup_id}
    index = v.id
    foodGroupId = v.foodGroup_id
    if type(foodGroupId) is str:

        foodGroupId = int(foodGroupId)
        print(v.id)
    if not math.isnan(foodGroupId):
        train_df[index] = obj
        food_id_list.append(v.id)
        print(v.id)
    else:
        test_df[index] = obj
        food_id_list.append(v.id)
        print(v.id)


def getRowInArrayByPropId(arr, foodId):
    for v in arr:
        if v["foodId"] == foodId:
            return v

    return None


nutrient_id_list = [203, 204, 205, 210, 212, 255, 301, 303, 304, 305, 306, 309, 312, 315, 401, 606, 608, 609, 610, 611,
                    613, 614, 636, 810, 827, 831, 832]

lnf = lnf[lnf["food_id"].isin(food_id_list)]
for i, v in lnf.iterrows():
    food_id = int(v.food_id)
    # if v.nutrient_id in nutrient_id_list:
    if train_df[food_id] != 0:
        train_df[food_id][str(v["nutrient_id"])] = v["value"]
    elif test_df[food_id] != 0:
        test_df[food_id][str(v["nutrient_id"])] = v["value"]

    # v_nutr_id = v.nutrient_id
    # if v_nutr_id in nutrient_id_list:

filter = train_df != 0
train_df = [elem for elem in train_df if elem != 0]
train_df = pd.DataFrame(train_df)

filter = test_df != 0
test_df = [elem for elem in test_df if elem != 0]
test_df = pd.DataFrame(test_df)


# train_df = pd.read_csv('C:\\dev\\perso\\simplenutritionfullstack\\Django\\machineLearning\\foodCategories\\input\\Result_22.csv')
# test_df = pd.read_csv('C:\\dev\\perso\\simplenutritionfullstack\\Django\\machineLearning\\foodCategories\\input\\Result_23.csv')


def fillNaWithZeros(set):
    for column in set.columns:
        set[column] = set[column].fillna(0)
    return set


train_df = fillNaWithZeros(train_df)

test_df = test_df.drop("foodGroup_id", axis=1)
test_df = fillNaWithZeros(test_df)

X_train = train_df.drop(["foodGroup_id","foodId"], axis=1)
Y_train = train_df["foodGroup_id"]
X_test = test_df.copy().drop(["foodId"], axis=1)

classifier = AdaBoostClassifier()
classifier.fit(X_train, Y_train)
predictions = classifier.predict(X_test)

test_df.insert(0, 'foodGroup_id', predictions)
test_df = test_df.transpose()

score = classifier.score(X_train, Y_train)

values = "UPDATE"
cpt = 0
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="secret123",
    port="3307",
  database="simplenutrition"
)
mycursor = mydb.cursor()
for v in test_df.iteritems():
    v = v[1]
    foodGroup_id = int(v["foodGroup_id"])
    id = int(v["foodId"])
    query = """UPDATE foods_food SET foodGroup_id = %s  WHERE id = %s """
    mycursor.execute(query, (foodGroup_id, id,),)
    mydb.commit()

for v in train_df.transpose().iteritems():
    v = v[1]
    foodGroup_id = int(v["foodGroup_id"])
    id = int(v["foodId"])
    query = """UPDATE foods_food SET foodGroup_id = %s  WHERE id = %s """
    try:
        mycursor.execute(query, (foodGroup_id, id,),)

        mydb.commit()
    except Exception:
        print("oops")



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

for classifier in classifiers:
    classifier.fit(X_train, Y_train)
    predictions = classifier.predict(X_test)
    score = classifier.score(X_train, Y_train)
    print(classifier.__class__.__name__ + " : " + str(score))


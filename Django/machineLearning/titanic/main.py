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
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier

from completing import completAge
from converting import *
from creating import *

train_df = pd.read_csv('C:\\dev\\perso\\simplenutritionfullstack\\Django\\machineLearning\\titanic\\input\\train.csv')
test_df = pd.read_csv('C:\\dev\\perso\\simplenutritionfullstack\\Django\\machineLearning\\titanic\\input\\test.csv')



combine = [train_df, test_df]

# tail = train_df.tail()
# describe = train_df.describe()
# describe2 = train_df.describe(include=['O'])

# pclass_correlation_test = train_df[['Pclass' ,'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)
# sibsp_corr_test = train_df[["SibSp", "Survived"]].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False)
# parch_corr_test = train_df[["Parch", "Survived"]].groupby(['Parch'], as_index=False).mean().sort_values(by='Survived', ascending=False)
#
# g = sns.FacetGrid(train_df, col='Survived')
# g.map(plt.hist, 'Age', bins=20)
#
# grid = sns.FacetGrid(train_df, col='Survived', size=2.2, aspect=1.6)
# grid.map(plt.hist, 'Sex', alpha=.5, bins=20)
# grid.add_legend()
#
# grid = sns.FacetGrid(train_df, col='Survived', row='Pclass', size=2.2, aspect=1.6)
# grid.map(plt.hist, 'Sex', alpha=.5, bins=20)
# grid.add_legend()
#
# grid = sns.FacetGrid(train_df,  size=2.2, aspect=1.6)
# grid.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette='deep')
# grid.add_legend()
#
# grid = sns.FacetGrid(train_df,row='Embarked',  size=2.2, aspect=1.6)
# grid.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette='deep')
# grid.add_legend()
#
# g = sns.FacetGrid(train_df, col='Survived')
# g.map(plt.hist, 'Fare', bins=5)


#completing
combine = completeFare(combine)

#CONVERTING
combine = convertSex(combine)
combine = convertFare(combine)

combine = completAge(combine)



#CREATING
combine = creatingTitle(combine)
combine = creatingFamily(combine)

test = train_df[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index=False).mean()

combine = convertAgeInCategory(combine)
combine = convertFareInCategory(combine)
combine = convertEmbarked(combine)

combine = creatingAgeClassFeature(combine)


# title_corr = train_df[["Title", "Survived"]].groupby(["Title"], as_index=False).mean().sort_values(by='Survived', ascending=False)
#
# test3 = pd.crosstab(train_df['Title'], train_df['Sex'])
#
# grid = sns.FacetGrid(train_df, row='Pclass', size=2.2, aspect=1.6)
# grid.map(plt.hist, 'Sex', alpha=.5, bins=20)
# grid.add_legend()

# train_df['AgeBand'] = pd.cut(train_df['Age'], 10)
# test4 = train_df[['AgeBand', 'Survived']].groupby(['AgeBand'], as_index=False).mean().sort_values(by='AgeBand', ascending=True)



#DROPPING
column_to_remove = ['Ticket', 'Cabin', 'Name','PassengerId', 'FamilySize']
train_df = train_df.drop(column_to_remove, axis=1)
test_df = test_df.drop(column_to_remove, axis=1)
combine = [train_df, test_df]

test = test_df.head(10)

X_train = train_df.drop("Survived", axis = 1)
Y_train = train_df["Survived"]
X_test = test_df.copy()


#logistic regression
logreg = LogisticRegression()
logreg.fit(X_train, Y_train)
acc_log = round(logreg.score(X_train, Y_train) * 100, 2)


# coeff_df = pd.DataFrame(train_df.columns.delete(0))
# coeff_df.columns = ['Feature']
# coeff_df["Correlation"] = pd.Series(logreg.coef_[0])
#
# coeff_df.sort_values(by='Correlation', ascending=False)


#svc
svc = SVC()
svc.fit(X_train, Y_train)
Y_pred = svc.predict(X_test)
acc_svc = round(svc.score(X_train, Y_train) * 100, 2)


# Decision Tree
decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, Y_train)
Y_pred = decision_tree.predict(X_test)
acc_decision_tree = round(decision_tree.score(X_train, Y_train) * 100, 2)


# Random Forest

random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, Y_train)
Y_pred = random_forest.predict(X_test)
random_forest.score(X_train, Y_train)
acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)



knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(X_train, Y_train)
Y_pred = knn.predict(X_test)
acc_knn = round(knn.score(X_train, Y_train) * 100, 2)



gaussian = GaussianNB()
gaussian.fit(X_train, Y_train)
Y_pred = gaussian.predict(X_test)
acc_gaussian = round(gaussian.score(X_train, Y_train) * 100, 2)



perceptron = Perceptron()
perceptron.fit(X_train, Y_train)
Y_pred = perceptron.predict(X_test)
acc_perceptron = round(perceptron.score(X_train, Y_train) * 100, 2)


sgd = SGDClassifier()
sgd.fit(X_train, Y_train)
Y_pred = sgd.predict(X_test)
acc_sgd = round(sgd.score(X_train, Y_train) * 100, 2)


linear_svc = LinearSVC()
linear_svc.fit(X_train, Y_train)
Y_pred = linear_svc.predict(X_test)
acc_linear_svc = round(linear_svc.score(X_train, Y_train) * 100, 2)



models = pd.DataFrame({
    'Model': ['Support Vector Machines', 'KNN', 'Logistic Regression',
              'Random Forest', 'Naive Bayes', 'Perceptron',
              'Stochastic Gradient Decent', 'Linear SVC',
              'Decision Tree'],
    'Score': [acc_svc, acc_knn, acc_log,
              acc_random_forest, acc_gaussian, acc_perceptron,
              acc_sgd, acc_linear_svc, acc_decision_tree]})
classement_lol = models.sort_values(by='Score', ascending=False)



plt.show()
print("hello")



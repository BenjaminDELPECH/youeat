from completing import *


def convertSex(combine):
    global dataset
    sex_mapping = {'male': 1, 'female': 0}
    for dataset in combine:
        dataset['Sex'] = dataset['Sex'].map(sex_mapping).astype(int)

    return combine


def convertAgeInCategory(combine):
    for dataset in combine:
        dataset.loc[dataset['Age'] <= 16, 'Age'] = 0
        dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
        dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
        dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
        dataset.loc[dataset['Age'] > 64, 'Age'] = 4
    return combine


def convertFareInCategory(combine):
    for dataset in combine:
        dataset.loc[dataset['Fare'] <= 7.91, 'Fare'] = 0
        dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1
        dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare'] = 2
        dataset.loc[dataset['Fare'] > 31, 'Fare'] = 3
        dataset['Fare'] = dataset['Fare'].astype(int)
    return combine


def convertFare(combine):
    # for dataset in combine:
    #     dataset['Fare'] = dataset['Fare'].astype(int)
    return combine


def convertEmbarked(combine):
    embarked_mapping = {'S': 0, 'C': 1, 'Q': 2}
    for dataset in combine:
        dataset = completeNaWithMostFreq(dataset, 'Embarked')
        dataset['Embarked'] = dataset['Embarked'].map(embarked_mapping).astype(int)
    return combine

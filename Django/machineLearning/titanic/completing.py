import numpy as np


def completAge(combine):
    global dataset
    guess_ages = np.zeros((2, 3))
    for dataset in combine:
        for i in range(0, 2):
            for j in range(0, 3):
                guess_df = dataset[(dataset['Sex'] == i) & (dataset['Pclass'] == (j + 1))]['Age'].dropna()

                age_guess = guess_df.median()
                guess_ages[i, j] = int(age_guess / 0.5 + 0.5) * 0.5

        for i in range(0, 2):
            for j in range(0, 3):
                dataset.loc[(dataset.Age.isnull()) & (dataset.Sex == i) & (dataset.Pclass == (j + 1)), 'Age'] = \
                    guess_ages[i, j]

        dataset['Age'] = dataset['Age'].astype(int)

    return combine

def completeFare(combine):
    for dataset in combine:
        dataset = completeNaWithMedianVal(dataset, 'Fare')
    return combine

def completeNaWithMostFreq(dataset, prop_name):
    mort_freq_port = dataset[prop_name].dropna().mode()[0]
    dataset[prop_name] = dataset[prop_name].fillna(mort_freq_port)
    return dataset

def completeNaWithMedianVal(dataset, prop_name):
    median = dataset[prop_name].dropna().median()
    dataset[prop_name] = dataset[prop_name].fillna(median)
    return dataset



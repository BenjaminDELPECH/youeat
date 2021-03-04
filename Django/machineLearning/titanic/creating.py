def creatingTitle(combine):
    global dataset
    title_mapping = {"Very Rare": 0, "Mrs": 1, "Miss": 2, "Master": 3, "Col": 4, "Major": 5, "Dr": 6, "Mr": 7,
                     "Rare unlucky": 8}
    for dataset in combine:
        dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
        # dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
        dataset['Title'] = dataset['Title'].replace(['Countless', 'Lady', 'Ms', 'Sir'], 'Very Rare')
        dataset['Title'] = dataset['Title'].replace(['Capt', 'Don', 'Jonkheer', 'Rev'], 'Rare unlucky')
        dataset['Title'] = dataset['Title'].replace(['Mlle', 'Mme', 'Ms'], 'Ms')
        dataset['Title'] = dataset['Title'].map(title_mapping)
        dataset['Title'] = dataset['Title'].fillna(0).astype(int)
    return combine



def creatingFamily(combine):
    for dataset in combine:
        dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1
        dataset['IsAlone']=0
        dataset.loc[dataset['FamilySize']==1, 'IsAlone']=1
    return combine

def creatingAgeClassFeature(combine):
    for dataset in combine:
        dataset['Age*Class'] = dataset.Age * dataset.Pclass

    return combine


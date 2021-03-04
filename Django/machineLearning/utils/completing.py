def completeNaWithZero(dataset, colum_list):
    for column in colum_list:
        dataset[column] = dataset[column].fillna(0)
    return dataset
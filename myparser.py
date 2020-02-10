import json
import sys
import yaml
import re
import pickle
import pandas as pd
import numpy as np

from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import fbeta_score, make_scorer, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def ParseFile(filename):
    filehandler = open(filename , 'rb')
    datastring = filehandler.read()
    datastring = datastring.decode("utf-8")
    datastring = re.sub(r'\'buffer\'\: \".*?\", ' , '' , datastring)
    datastring = re.sub('\"' , '' , datastring)
    datastring = re.sub(r'\'buffer\'\: \'.*?\', ' , '' , datastring)
    datastring = re.sub('\'' , '\"' , datastring)
    data = yaml.load(datastring)
    # Got list calls
    listcalls = []
    for item in data[1]['calls']:
        listcalls.append(item['api'])
    # filehandler = open(filename + '.listcalls' , 'w')
    # filehandler.write(str(listcalls))
    # filehandler.close()

    return listcalls

def PrepareListCalls(listcalls):
    if len(listcalls) < 50:
        return listcalls
    i = 1
    while True:
        if i >= len(listcalls): 
            break
        while listcalls[i] == listcalls[i-1]:
            del listcalls[i]
            if i == len(listcalls): 
                break
        i += 1
    return listcalls

def WriteInCsv(listcalls , mapping):
    encoded = ''
    i = 0
    for line in mapping:
        '''
        try:
            en = mapping[line]
        except:
            en = 0
        '''
        if line == '':
            continue
        if line in listcalls :
            en = mapping[line]
        else :
            en = 0
        encoded += str(int(en)) + ','
        i += 1
    # print('Iter = ' + str(i))
    with open('report.csv', 'w') as f:
        title = ''
        j = 0
        for i in range(len(mapping) - 1):
            title += str(int(i)) + ','
            j += 1
        # print('Iter = ' + str(j))
        f.write(title[:-1] + '\n')
        f.write(encoded[:-1] + '\n') 

def ReadCSV(name, value, limit):
    dataset = pd.read_csv(name, nrows=limit , dtype = 'int64')
    # X = dataset.sample(frac=1).drop(dataset.columns[[0, 1, 2]], axis=1)
    X_selection = dataset.fillna(0)
    X = X_selection.values
    if   value == 1: y = np.ones((len(X), 1))
    elif value == 0: y = np.zeros((len(X), 1))
        
    return X, y

def ReadTestData():
    X, y = ReadCSV('report.csv', 0, 2000)
    return X,y

def RunClassifier(classifier  ,  testX) :
    y_pred = int(classifier.predict(testX[0])[0])
    return y_pred

def InitClassifier() :
    with open('mapping.pickle', 'rb') as f:
        mapping = pickle.load(f)
    with open('X.pickle', 'rb') as f:
        X = pickle.load(f)
    with open('y.pickle', 'rb') as f:
        y = pickle.load(f)
    classifier = RandomForestClassifier(n_estimators=80, random_state=17, criterion = 'entropy')
    classifier.fit(X, y.ravel())
    return classifier , mapping 

def GetListCalls(data) :
    # Got list calls
    listcalls = []
    for item in data[1]['calls']:
        listcalls.append(item['api'])
    return listcalls

def StartParsing(processes , score) :
    print(str(score))
    classifier , mapping = InitClassifier()
    listcalls = GetListCalls(processes)
    listcalls = PrepareListCalls(listcalls)
    WriteInCsv(listcalls, mapping)
    testX = ReadTestData()
    res =  RunClassifier(classifier , testX)
    if res == 1 :
        print('Malware')
    elif res == 0 :
        print('Clear')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
from copy import copy, deepcopy
import numpy as np
import pandas as pd

def classify(outfile, X_train, X_test,y_train,y_test,X_test_with_id):
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    mlp = MLPClassifier(hidden_layer_sizes=(40,40,40))
    mlp.fit(X_train,y_train)
    predictions = mlp.predict(X_test)
    prediction = pd.DataFrame(predictions, columns=['predictions']).to_csv('prediction.csv')

    output_file = open(outfile,'w')
    for i in range(0,len(X_test)):
        #the string to be written is the crown id + classification
        temp = str(X_test_with_id[i][0]) + ", " + str(X_test_with_id[i][1]) + ", " + str(predictions[i]) + "\n"
        output_file.write(temp)
    output_file.close()
    print confusion_matrix(y_test,predictions)
    print classification_report(y_test,predictions)
    log_y_prob  = mlp.predict_log_proba(X_test)
    y_prob = mlp.predict_proba(X_test)
    return predictions


training_data_file = open('hyper_bands_train.csv','r')
specied_id_file = open('species_id_train.csv','r')
hyperbands = []
id_dictionary = {}
crown_id_dictionary = {}
answers = []
answers_genus = []
first = True
others = []
for line in specied_id_file:
    if first:
        first = False
        continue
    if 'other' in line or 'Other' in line:
        others.append(line.rstrip().split(',')[0])
    id_dictionary.update({line.rstrip().split(',')[0]:line.rstrip().split(',')[3:5]})

first = True
iteration = 0
for line in training_data_file:
    if first:
        first = False
        continue
    row = line.rstrip().split(',')
    if row[0] in others:
        continue
    answers.append( id_dictionary.get( row[0] ) )
    row.append(iteration)
    row.insert(0,iteration)
    hyperbands.append(row)
    iteration = iteration + 1


X = hyperbands
y = answers

X_train, X_test, y_train, y_test = train_test_split(X, y)
y_gen_train = []
y_sp_train = []
y_gen_test = []
y_sp_test = []
for row in y_test:
    y_gen_test.append(row[0])
for row in y_test:
    y_sp_test.append(row[1])
for row in y_train:
    y_gen_train.append(row[0])
for row in y_train:
    y_sp_train.append(row[1])

X_train_with_id = deepcopy(X_train)
for row in X_train:
    del row[0:2]

X_test_with_id = deepcopy(X_test)
for row in X_test:
    del row[0:2]

p1 = classify('out1.csv',X_train,X_test,y_sp_train,y_sp_test,X_test_with_id)
p2 = classify('out2.csv',X_train,X_test,y_gen_train,y_gen_test,X_test_with_id)
print p1
print p2

a = pd.read_csv('out1.csv')
b = pd.read_csv('out2.csv')
b = b.dropna(axis=1)
merged = a.merge(b)
merged.to_csv("output.csv", index=False)

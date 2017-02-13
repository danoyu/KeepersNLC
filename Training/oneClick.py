'''
Created on Feb 12, 2017

@author: חנן ליפסקין
'''
import training
import classifier
import accuracy
import os
from classifier import delete_by_id_classifiers, list_classifiers_name_id

filename = '../csv_files/ownDB_good_level_of_bad.csv'
nb = [10,20,30,40,50]

def exe_1_level(file_name,nb):
    classifier.delete_by_id_classifiers()
    training.create_training_files(file_name,nb)
    classifier.create_list_classifiers(file_name)
    print(classifier.list_classifiers_name_id())
    accuracy.create_graph(file_name)

#print(classifier.list_classifiers_name_id())
#classifier.delete_by_id_classifiers()
exe_1_level(filename,nb)  

def exe_2_levels(file_name,nb):
    classifier.delete_by_id_classifiers()
    training.create_training_files(file_name,nb)
    classifier.create_list_classifiers(file_name)
    print(classifier.list_classifiers_name_id())
    accuracy.create_graph(file_name)
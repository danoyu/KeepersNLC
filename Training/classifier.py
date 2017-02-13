'''
Created on Feb 8, 2017

@author: חנן ליפסקין
'''

#===============================================================================
# SCRIPTS FOR CREATE NEW CLASSIFIERS FROM THE WATSON NLC SERVICE AND MANIPULATE IT
# THE INPUT FOR CREATE A CLASSIFIER MUST BE A .CSV FILE 
#===============================================================================



import json
import time
from watson_developer_cloud import NaturalLanguageClassifierV1
import os

nb = [10,20,30,40,50]
#classifier_id='cedf17x168-nlc-3397' 
classifier_smallexp_id='cedec3x167-nlc-4394'

nlc_usr="1b9c3479-17e2-41d6-a37c-57d3c2652b46" #user of NLC
nlc_psw="1JDTIomXVdi3"  #password of NLC

file = "training_set.csv"
nameDir = '../training_csv_files/'

natural_language_classifier = NaturalLanguageClassifierV1(
  username=nlc_usr,
  password=nlc_psw)



#CREATE A NEW CLASSIFIER

#===============================================================================
#The training data must have at least five records (rows) and no more than 15,000 records
def create_classifier(training_file,name):
    with open(training_file, 'rb') as training_data:
            t = time.clock()
            classifier = natural_language_classifier.create(
                    training_data=training_data,
                    name=name,
                    language="en")
            t = time.clock() - t
    print('creating time : ' + str(t))
    return classifier
#===============================================================================

#CONSULT LIST OF CLASSIFIER AVAILABLE 

#create_classifier('../training_csv_files/training_50.csv','class1')

#list all the id classifiers
def list_classifiers_name_id():
    classifiers = natural_language_classifier.list()
    list_classifiers = dict()
    x = json.dumps(classifiers,indent =2)
    jsonparser = json.loads(x)
    classi = jsonparser['classifiers']
    for i in range(len(classi)):
        list_classifiers[classi[i]['name']] = classi[i]['classifier_id']
    return list_classifiers

#print(list_classifiers_name_id())


#list all the id of the classifiers
def list_classifiers_id():
    classifiers = natural_language_classifier.list()
    list_classifiers = list()
    x = json.dumps(classifiers,indent =2)
    jsonparser = json.loads(x)
    classi = jsonparser['classifiers']
    for i in range(len(classi)):
        list_classifiers.append(classi[i]['classifier_id'])
    return list_classifiers

#print(list_classifiers_id())


#delete all the classifiers by the name
def delete_by_name_classifiers():
    ids = list_classifiers_name_id()
    for id in ids:
        natural_language_classifier.remove(ids[id])
    
#delete_by_name_classifiers()

#print(list_classifiers_name_id())
#delete all the classifiers by id
def delete_by_id_classifiers():
    ids = list_classifiers_id()
    for id in ids:
        natural_language_classifier.remove(id)
    
#delete_by_id_classifiers()


#create a list of classifiers
def create_list_classifiers(filename):
    #0.05 only 2 records not enough
    i=0
    files = os.listdir('../training_csv_files')
    filename = filename.split('/')
    filename = filename[len(filename)-1]
    filename = filename.split('.')[0]
    print(filename)
    for file in files:
        if file.__contains__(filename):
            nb = file.split('_')
            nb = nb[len(nb) - 1]
            nb = nb.split('.')[0]
            name_classifier = filename + '_classifier_' + nb
            create_classifier('../training_csv_files/' + file,name_classifier)


def get_id_classifier(name):
    ids = list_classifiers_name_id()
    return ids[name]

def get_status(name):
    id = get_id_classifier(name)
    return natural_language_classifier.status(id)['status']

#print(get_status('ownDB_good_level_of_bad_classifier_40'))
#create_list_classifiers('training')

#delete_by_id_classifiers()
#print(list_classifiers_name_id())

#print(list_classifiers_name_id())





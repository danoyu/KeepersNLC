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


# classifier_id='cedf17x168-nlc-3397' 
#classifier_smallexp_id = 'cedec3x167-nlc-4394'

# nlc_usr="1b9c3479-17e2-41d6-a37c-57d3c2652b46" #user of NLC
# nlc_psw="1JDTIomXVdi3"  #password of NLC

#nlc_usr = '96e6ee96-1661-4aae-9956-c07db9eef464'
#nlc_psw = 'v2nb6hPx87JH'

nlc_usr = '5567e74f-8ed1-4427-810b-de1211d63b5e'
nlc_psw = 'GgcTiEDqydS7'

file = "training_set.csv"
nameDir = '../training_csv_files/'

natural_language_classifier = NaturalLanguageClassifierV1(
  username=nlc_usr,
  password=nlc_psw)



# CREATE A NEW CLASSIFIER

#===============================================================================
# The training data must have at least five records (rows) and no more than 15,000 records
def create_classifier(training_file, name, nb = None):
    #print ('Name of the new classifier : ' , name)
    #print('Training with',nb , 'percent with the file', training_file)
    print(list_classifiers_name_id())
    print(len(list_classifiers_name_id()))
    with open(training_file, 'rb') as training_data:
            t = time.clock()
            classifier = natural_language_classifier.create(
                    training_data=training_data,
                    name=name,
                    language="en")
            t = time.clock() - t
    #print('creating time : ' + str(t))
    status = get_status(name)
    t = time.clock()
    #while status != 'Available':
    #    status = get_status(name)
    #t = time.clock() - t
    #print('traning time : ' + str(t))
    return classifier
#===============================================================================

# CONSULT LIST OF CLASSIFIER AVAILABLE 

# create_classifier('../training_csv_files/training_50.csv','class1')

# list all the id classifiers
def list_classifiers_name_id():
    classifiers = natural_language_classifier.list()
    list_classifiers = dict()
    x = json.dumps(classifiers, indent=2)
    jsonparser = json.loads(x)
    classi = jsonparser['classifiers']
    for i in range(len(classi)):
        list_classifiers[classi[i]['name']] = classi[i]['classifier_id']
    return list_classifiers

# print(list_classifiers_name_id())


# list all the id of the classifiers
def list_classifiers_id():
    classifiers = natural_language_classifier.list()
    list_classifiers = list()
    x = json.dumps(classifiers, indent=2)
    jsonparser = json.loads(x)
    classi = jsonparser['classifiers']
    for i in range(len(classi)):
        list_classifiers.append(classi[i]['classifier_id'])
    return list_classifiers

# print(list_classifiers_id())


# delete all the classifiers by the name
def delete_by_name_classifiers():
    ids = list_classifiers_name_id()
    for id in ids:
        natural_language_classifier.remove(ids[id])
    
# delete_by_name_classifiers()

# print(list_classifiers_name_id())
# delete all the classifiers by id
def delete_by_id_classifiers():
    ids = list_classifiers_id()
    for id in ids:
        natural_language_classifier.remove(id)
    
# delete_by_id_classifiers()


# create a list of classifiers
def create_list_classifiers(filename):
    files = os.listdir('../training_csv_files')
    filename = filename.split('/')
    filename = filename[len(filename) - 1]
    filename = filename.split('.')[0]
    for file in files:
        if file.__contains__(filename):
            nb = file.split('_')
            nb = nb[len(nb) - 1]
            nb = nb.split('.')[0]
            name_classifier = file.split('.csv')[0] + '_classifier_' + nb
            create_classifier('../training_csv_files/' + file, name_classifier,nb)
          

def get_id_classifier(name):
    ids = list_classifiers_name_id()
    return ids[name]

def get_status(name):
    id = get_id_classifier(name)
    return natural_language_classifier.status(id)['status']
        
# class a sentence with the classifier classifier_name
def classify(classifier_name, sentence):
    classifiers = list_classifiers_name_id()
    
    # API CALL 
    natural_language_classifier = NaturalLanguageClassifierV1(
    username=nlc_usr, password=nlc_psw)
    t = time.clock()
    classes = natural_language_classifier.classify(classifiers[classifier_name], sentence)
    t = time.clock() - t
    print('API call time : ' , str(t))
    myjson = json.dumps(classes)
                 
    # Parsing 
    jsonparser = json.loads(myjson);  # parse the ans of the api
    answer_class = jsonparser["classes"][0]["class_name"]  # classified class with more confidence 
    # print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                
    return answer_class

# print(classify('classifier_20', 'this is fucking hell'))
# print(get_status('ownDB_good_level_of_bad_classifier_40'))
# create_list_classifiers('training')

# delete_by_id_classifiers()
# print(list_classifiers_name_id())

# print(list_classifiers_name_id())





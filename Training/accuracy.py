'''
Created on Feb 9, 2017

@author: חנן ליפסקין
'''
import training_classifier
import csv,json
import os
from watson_developer_cloud import NaturalLanguageClassifierV1
from training_classifier import natural_language_classifier
 
#===============================================================================
# TEST WITH SMALL REAL EXAMPLES RANDOMED CLASSIFIED. 
# >> THE INPUT IS A .CSV FILE WITH THE TEXT,CLASS FORMAT 
# O  THE PROCESS IS:
#    LOOP FOR ALL THE EXAMPLES:
#     1- TAKE AN EXAMPLE THAT WE ALREADY KNOW THE CLASS,
#     2- ASK THE API FOR THE CLASS 
#     3- COMPARE RESULT
#     4- COUNT THE HITS 
# << THE OUTPUT IS THE ACCURACY OF THE CLASSIFIER 
#===============================================================================



#variables using inside the code 
nlc_usr="1b9c3479-17e2-41d6-a37c-57d3c2652b46" #user of NLC
nlc_psw="1JDTIomXVdi3"  #password of NLC
counter=0 #counter number of hits
n_row=0 #number of examples into the file 

file = "training_set.csv"
nameDir = '../training_csv_files/'

#class a sentence with the classifier name_classifier
def classify(name_classifier,sentence):
    classifiers = training_classifier.list_classifiers_name_id()
    #API CALL 
    natural_language_classifier = NaturalLanguageClassifierV1(
    username=nlc_usr, password=nlc_psw)
    classes = natural_language_classifier.classify(classifiers[name_classifier], sentence)
    myjson=json.dumps(classes)
                 
    # Parsing 
    jsonparser=json.loads(myjson); #parse the ans of the api
    answer_class= jsonparser["classes"][0]["class_name"]  #classified class with more confidence 
    #print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                
    return answer_class

#print(classify('classifier_20', 'this is fucking hell'))
    

def test(nameDir):
    #classifiers = training_classifier.classifiers_id()
    files = os.listdir(nameDir)
    classifiers = training_classifier.list_classifiers_name_id()
    accuracies = list()
    graph = dict()
    for name_classifier in classifiers:
        print(str(name_classifier).upper())
        for file in files:
            #print('training file : ' + nameDir + file)
            file_name = nameDir + file
            with open(file_name) as csvfile:
                n_row = 0
                counter = 0
                reader=csv.reader(csvfile)
            
                #star process 
                for row in reader:
                    n_row += 1 #number of examples into the file 
                    actual_sentence=row[0] # string of the example
                    actual_class=row[1]  #example that we already know  the class
            
                    answer_class= classify(name_classifier, actual_sentence)  #classified class with more confidence 
                    #print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                
                    if actual_class == answer_class: #asking for a hit
                        counter=counter + 1
                        
            accuracy=(counter/n_row)*100
            accuracies.append(accuracy)
            print("Results: ", "\n" , "Number of examples: ", n_row, "\n", "Number of hits: ",counter, '\n', "Accuracy: ", accuracy,"%");   
        
test(nameDir)


def test_f(nameDir):
    #classifiers = training_classifier.classifiers_id()
    files = os.listdir(nameDir)
    classifiers = training_classifier.list_classifiers_name_id()
    accuracies = list()
    graph = dict()
    for file in files:
        file_name = nameDir + file
        with open(file_name) as csvfile:
            for name_classifier in classifiers:
            #print('training file : ' + nameDir + file)
                n_row = 0
                counter = 0
                reader=csv.reader(csvfile)
                #star process 
                for row in reader:
                    n_row += 1 #number of examples into the file 
                    actual_sentence=row[0] # string of the example
                    actual_class=row[1]  #example that we already know  the class
                                                  
                    answer_class= classify(name_classifier, actual_sentence)  #classified class with more confidence 
                    #print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                                
                    if actual_class == answer_class: #asking for a hit
                        counter=counter + 1
                                        
                accuracy=(counter/n_row)*100
                accuracies.append(accuracy)
            print("Results: ", "\n" , "Number of examples: ", n_row, "\n", "Number of hits: ",counter, '\n', "Accuracy: ", accuracy,"%");   
        
test_f(nameDir)

#test sur un fichier tout avec tout les classifiers 
def test_fichier(file_name,training_file,source_file):
    #classifiers = training_classifier.classifiers_id()
    classifiers = training_classifier.list_classifiers_name_id()
    accuracies = list()
    graph = dict()
    with open(file_name) as csvfile:
        for name_classifier in classifiers:
            #print('training file : ' + nameDir + file)
                n_row = 0
                counter = 0
                reader=csv.reader(csvfile)
                #star process 
                for row in reader:
                    n_row += 1 #number of examples into the file 
                    actual_sentence=row[0] # string of the example
                    actual_class=row[1]  #example that we already know  the class
                                                  
                    answer_class= classify(name_classifier, actual_sentence)  #classified class with more confidence 
                    #print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                                
                    if actual_class == answer_class: #asking for a hit
                        counter=counter + 1
                                        
                accuracy=(counter/n_row)*100
                accuracies.append(accuracy)
    print("Results: ", "\n" , "Number of examples: ", n_row, "\n", "Number of hits: ",counter, '\n', "Accuracy: ", accuracy,"%");   
        
test_fichier(nameDir)


# retrainnig problem
# emoticons
# time consuming for training testing

'''
Created on Feb 12, 2017

@author: חנן ליפסקין
'''

#===============================================================================
# TEST WITH SMALL REAL EXAMPLES RANDOMED CLASSIFIED. 
# >> THE INPUT IS A .CSV FILE WITH THE TEXT,CLASS FORMAT 
# O  THE PROCESS IS:
#    LOOP FOR ALL THE EXAMPLES:
#     1- TAKE AN EXAMPLE OF THE FILE WITH GOOD AND BAD EXAMPLES, THAT WE ALREADY KNOW THE CLASS 
#     2- ASK THE FIRST CLASSIFIER (GOOD-BAD CLASSIFIER) IF IT IS A GOOD OR BAD SENTENCE
#     3- IF IT IS BAS ASK THE SECOND CLASSIFIER (LEVEL-CLASSIFIER) FOR THE CLASS (LEVEL OF THE SENTENCE) 
#     4- COMPARE RESULT
#     5- COUNT THE HITS 
# << THE OUTPUT IS THE ACCURACY OF THE CLASSIFIER 
#CLARIFICATION:
#FILE 1 -> CLASSIFIER 1 GOOD-BAD EXAMPLES
#FILE 2 -> CLASSIFIER 2 LEVEL OF BAD EXAMPPLES 
#===============================================================================

import csv,json
from watson_developer_cloud import NaturalLanguageClassifierV1
import training_classifier
import accuracy as acc
import Training_set
from Training_set import create_training_file_balance_good_bad

#variables using inside the code 
classifier_id='f5bbbbx174-nlc-871' #classifier id for the good-bad classifier 
classifier_id_2='cedd09x164-nlc-4340' #classifier id for the bad-level classifier
 
nlc_usr="1b9c3479-17e2-41d6-a37c-57d3c2652b46" #user of NLC
nlc_psw="1JDTIomXVdi3"  #password of NLC

file_bad="../csv_files/ownDB_good_level_of_bad.csv" #name of the file with all the good-bad examples 
file_0_1="../csv_files/2ls_ownDB.csv" #name of the file with all the bad examples

class_2="";
classifier_0_1 = 'classifier_0_1'
classifier_bad = 'classifier_bad'

#create 2 classifiers :
#1 to class 0 or 1
#2 to class 1,2,3 levels of bad
def create2ls_classifiers(file_0_1,file_bad,name_0_1,name_bad):
    classifier_0_1 = training_classifier.create_classifier(file_0_1, name_0_1)
    classifier_bad = training_classifier.create_classifier(file_bad,name_bad)
    
#create2ls_classifiers(file_0_1, file_bad, classifier_0_1, classifier_bad)

def accuracy(testing_file,classifier_0_1,classifier_bad):
    # open csvs file (with all the examples file 1 and file 2 see notes top on the page )
    flag=False;
    counter1=0 #counter number of hits in the good-bad classifier 
    counter2=0 #counter number of hits in the level-classifier
    counter_get_2=0 #counter the number of time that the algorithm get into the level-classifier
    bad=1 # number to identify the bad class into the good-bad classifier 
    counter = 0
    n_row = 0
    with open(testing_file) as csvfile:
        reader=csv.reader(csvfile,delimiter=',')
        
        #star process 
        for row in reader:
            n_row=n_row+1 #number of examples into the file 
            print(n_row)
            actual_sentence=row[0] # string of the example
            actual_class=row[1]  #example that we already know  the class
            
            #API CALL TO THE GOOD-BAD CLASSIFIER 
            ans_class_name = acc.classify(classifier_0_1, actual_sentence)
            if ans_class_name == 1:
                #API CALL TO THE LEVEL-CLASSIFIER          
                ans_class_name = acc.classify(classifier_bad, actual_sentence)
            print("GOOD-BAD CLASSIFIER: ","Actual Class: ",actual_class," ","Response Class: ",ans_class_name,"\n")    
            
            if actual_class == ans_class_name: #asking for a hit
                counter += 1
        
            
    accuracy = (counter/n_row)*100
    print("Number of examples: ", n_row ,"\n","Number of hits ",counter,"\n", "Accuracy: ", accuracy,"%","\n")  

accuracy(file_bad, classifier_0_1, classifier_bad)

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
# CLARIFICATION:
# FILE 1 -> CLASSIFIER 1 GOOD-BAD EXAMPLES
# FILE 2 -> CLASSIFIER 2 LEVEL OF BAD EXAMPPLES 
#===============================================================================

import classifier
import csv
import accuracy as acc
import training

file_bad = "../csv_files/ownDB_good_level_of_bad.csv"  # name of the file with all the good-bad examples 
file_0_1 = "../csv_files/2ls_ownDB.csv"  # name of the file with all the bad examples

classifier_0_1 = 'classifier_0_1'
classifier_bad = 'classifier_bad'

file_name = "../csv_files/ownDB_good_level_of_bad.csv"
#training_0_1 = '../training_csv_files/training_0_1'
#training_bad = '../training_csv_files/training_bad'

# create 2 classifiers :
# 1 to class 0 or 1
# 2 to class 1,2,3 levels of bad
#with a file with 4 classes
def create2ls_classifiers2(file_name, name_0_1, name_bad,p):
    name = file_name.split('.csv')[0]
    file_0_1 = name +'_0_1.csv'
    file_bad = name + '_BAD.csv'
    training.create_file_0_1(file_name, file_0_1)
    training.create_file_bad(file_name, file_bad)
    name = name.split('/')
    name = name[len(name)-1]
    training_0_1 = '../training_csv_files/' + name + '_training_0_1.csv'
    training_bad = '../training_csv_files/' + name + '_training_BAD.csv'
    training.create_training_file_balance_good_bad(file_0_1,p,training_0_1)
    training.create_training_file_random(file_bad,p, training_bad)
    classifier.create_classifier(training_0_1, name_0_1)
    classifier.create_classifier(training_bad, name_bad)

#classifier.delete_by_id_classifiers()
#create2ls_classifiers2(file_name, classifier_0_1, classifier_bad,0.4)
#print classifiers with names
print(classifier.list_classifiers_name_id())

#give the accuracy based on the 2 levels solutions
def accuracy(testing_file, classifier_0_1, classifier_bad):
    # open csvs file (with all the examples file 1 and file 2 see notes top on the page )
    counter_get_2 = 0  # counter the number of time that the algorithm get into the level-classifier
    counter = 0
    n_row = 0
    with open(testing_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        # star process 
        for row in reader:
            n_row += 1  # number of examples into the file 
            actual_sentence = row[0]  # string of the example
            actual_class = row[1]  # example that we already know  the class
            
            # API CALL TO THE GOOD-BAD CLASSIFIER 
            ans_class_name = acc.classify(classifier_0_1, actual_sentence)
            
            if ans_class_name == '1':
                counter_get_2 += 1
                # API CALL TO THE LEVEL-CLASSIFIER 
                ans_class_name = acc.classify(classifier_bad, actual_sentence)
            print("CLASSIFIER: ", "Actual Class: ", actual_class, " ", "Response Class: ", ans_class_name, "\n")    
            
            if actual_class == ans_class_name:  # asking for a hit
                counter += 1
        
    print(counter_get_2)
    accuracy = (counter / n_row) * 100
    print("Number of examples: ", n_row , "\n", "Number of hits ", counter, "\n", "Accuracy: ", accuracy, "%", "\n")  

accuracy(file_bad, classifier_0_1, classifier_bad)

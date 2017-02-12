'''
Created on Feb 9, 2017

@author: חנן ליפסקין
'''
import training_classifier
import csv, json
import os
from watson_developer_cloud import NaturalLanguageClassifierV1
import matplotlib.pyplot as plt

 
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



# variables using inside the code 
nlc_usr = "1b9c3479-17e2-41d6-a37c-57d3c2652b46"  # user of NLC
nlc_psw = "1JDTIomXVdi3"  # password of NLC
counter = 0  # counter number of hits
n_row = 0  # number of examples into the file 

file = "training_set.csv"
nameDir = '../training_csv_files/'
file_name = '../csv_files/2ls_ownDB.csv'

# class a sentence with the classifier classifier_name
def classify(classifier_name, sentence):
    classifiers = training_classifier.list_classifiers_name_id()
    
    # API CALL 
    natural_language_classifier = NaturalLanguageClassifierV1(
    username=nlc_usr, password=nlc_psw)
    classes = natural_language_classifier.classify(classifiers[classifier_name], sentence)
    myjson = json.dumps(classes)
                 
    # Parsing 
    jsonparser = json.loads(myjson);  # parse the ans of the api
    answer_class = jsonparser["classes"][0]["class_name"]  # classified class with more confidence 
    # print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                
    return answer_class

#print(classify('classifier_20', 'this is fucking hell'))
    
# give the accuracy of 1 classifier for the testing_file
def accuracy(testing_file, classifier_name):
    #print(file_name)
    #print(str(classifier_name).upper())
    with open(testing_file) as csvfile:
            n_row = 0
            counter = 0
            reader = csv.reader(csvfile)
            # star process 
            for row in reader:
                    n_row += 1  # number of examples into the file 
                    actual_sentence = row[0]  # string of the example
                    actual_class = row[1]  # example that we already know  the class
                                                  
                    answer_class = classify(classifier_name, actual_sentence)  # classified class with more confidence 
                    #print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                                
                    if actual_class == answer_class:  # asking for a hit
                        counter = counter + 1
                        
            accuracy = (counter / n_row) * 100
            print("Results: ", "\n" , "Number of examples: ", n_row, "\n", "Number of hits: ", counter, '\n', "Accuracy: ", accuracy, "%");   
    return accuracy

#accuracy(file_name,'classifier_50')


#give the accuracies of all the classifiers for the testing_file
#return a dictionnary with the classifier and his accuracy
def test(testing_file):
    classifiers = training_classifier.list_classifiers_name_id()
    accuracies = list()
    data = dict()
    for classifier_name in classifiers:
        print(str(classifier_name).upper())
        accur = accuracy(testing_file, classifier_name)
        accuracies.append(accur)
        data[classifier_name] = accur
    return data

#print(test(file_name))

#create a graph with data
def create_graph_with_data(data):
    graph = dict()
    for name in data:
        p = int(name.split('classifier_')[1])
        graph[p] = data[name]
    return graph
    

#data = {'classifier_10': 70, 'classifier_20': 77, 'classifier_30': 80}
#create_graph_with_data(data)

#data = {'classifier_50': 88.23529411764706, 'classifier_10': 70.58823529411765, 'classifier_20': 70.58823529411765, 'classifier_30': 76.47058823529412, 'classifier_40': 86.27450980392157}
#graph = {40: 86.27450980392157, 50: 88.23529411764706, 20: 70.58823529411765, 10: 70.58823529411765, 30: 76.47058823529412}


def create_graph(testing_file):
    data = test(testing_file)
    graph = create_graph_with_data(data)
    print(graph)
    plt.xlabel('percent of DB')
    plt.ylabel('accuracy')
    plt.plot(*zip(*sorted(graph.items())))
    plt.show()
    
#create_graph(file_name)



# retrainnig problem
# emoticons
# time consuming for training testing


    
#print(os.listdir('../csv_files'))



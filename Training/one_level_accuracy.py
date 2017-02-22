'''
Created on Feb 9, 2017

@author: חנן ליפסקין
'''
import classifier
import csv, json
import os
from watson_developer_cloud import NaturalLanguageClassifierV1
import matplotlib.pyplot as plt
import time
from matplotlib.pyplot import xlabel, ylabel

 
#===============================================================================
# create_datas WITH SMALL REAL EXAMPLES RANDOMED CLASSIFIED. 
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
# nlc_usr = "1b9c3479-17e2-41d6-a37c-57d3c2652b46"  # user of NLC
# nlc_psw = "1JDTIomXVdi3"  # password of NLC

nlc_usr = '96e6ee96-1661-4aae-9956-c07db9eef464'
nlc_psw = 'v2nb6hPx87JH'

file = "training_set.csv"
file_name = '../csv_files/2ls_ownDB.csv'


    
# give the accuracies of 1 classifier for the testing_file
def accuracy2(testing_file, classifier_name):

    with open(testing_file) as csvfile:
            n_row = 0
            counter = 0
            reader = csv.reader(csvfile)
            false_alerts_counter = 0 #number of predictions is 1,2 or 3 and the actual class is 0
            missplaced_alerts_counter = 0 #number of 
            missed_alerts_counter = 0 #number of predictions is 0 and the actual class is 1,2 or 3
            A = 0 # All that the prediction is different of 0
            T_1_2_3 = 0
            T_0 = 0
            # star process 
            for row in reader:
                    n_row += 1  # number of examples into the file 
                    actual_sentence = row[0]  # string of the example
                    actual_class = row[1]  # example that we already know  the class
                                                  
                    answer_class = classifier.classify(classifier_name, actual_sentence)  # classified class with more confidence 
                    print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                    if actual_class == '0':
                        T_0 += 1
                    if actual_class == answer_class:  # asking for a hit
                        counter = counter + 1
                        #good prediction different of 0(missplaced_alert)
                        if actual_class != '0': 
                            missplaced_alerts_counter += 1  
                    #if the prediction is wrong        
                    else :
                        #when the class is 0 and the prediction is different of 0(false alert)
                        if actual_class == '0':
                            false_alerts_counter += 1
                        #when the actual class is 1,2 or 3 and it predict 0
                        if answer_class == '0': #else is ok too i think need to see 
                            missed_alerts_counter += 1
            
                    #when the prediction is different of 0
                    if answer_class != '0':
                        A += 1
            
            accuracy = (counter / n_row) * 100
            print('A : ', A)
            print('false alerts counter :' ,false_alerts_counter)
            print('missplaced alerts counter :', missplaced_alerts_counter)
            print('missed alerts counter :', missed_alerts_counter)
            false_alerts = (false_alerts_counter / A) *100
            missplaced_alerts = ((A - missplaced_alerts_counter)/A)  * 100
            T_1_2_3 = n_row - T_0
            print('T_1_2_3 : ' , T_1_2_3)
            missed_alert = (missed_alerts_counter/T_1_2_3) * 100
            
            
            print("Results: ", "\n" , "Number of examples: ", n_row, "\n", "Number of hits: ", counter, '\n', "Accuracy: ", accuracy, "%",'\n', "False Alerts: ", false_alerts, "%",'\n', "Missplaced Alerts: ", missplaced_alerts, "%",'\n', "Missed Alerts: ", missed_alert, "%");   
            
    return accuracy,false_alerts,missplaced_alerts,missed_alert

# give the accuracies of all the classifiers for the testing_file
# return a dictionnary with the classifier and his accuracy
def create_datas(testing_file,nb):
    classifiers = classifier.list_classifiers_name_id()
    accuracies = list()
    false = list()
    missplaced = list()
    missed = list()
    data_accur = dict()
    data_false = dict()
    data_missplaced = dict()
    data_missed = dict()  
    for num in nb:
        for classifi in classifiers:
            if(classifi.__contains__(str(num))):
                classifier_good_bad = classifi
        #print(testing_file)
        #print(classifier_good_bad)
        accur, false_alerts, missplaced_alerts, missed_alert = accuracy2(testing_file, classifier_good_bad)
        accuracies.append(accur)
        missplaced.append(missplaced_alerts)
        missed.append(missed_alert)
        false.append(false_alerts)
        data_accur[num] = accur
        data_false[num] = false_alerts
        data_missplaced[num] = missplaced_alerts
        data_missed[num] = missed_alert
    return data_accur,data_false,data_missplaced,data_missed

# print(create_datas(file_name))

# create a graph with data
def create_graph_with_data(data):
    graph = dict()
    for name in data:
        p = int(name.split('classifier_')[1])
        graph[p] = data[name]
    return graph
    
def show_graph(graph,title,xlabel,ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(*zip(*sorted(graph.items())))
    
# data = {'classifier_10': 70, 'classifier_20': 77, 'classifier_30': 80}
# create_graph_with_data(data)

# data = {'classifier_50': 88.23529411764706, 'classifier_10': 70.58823529411765, 'classifier_20': 70.58823529411765, 'classifier_30': 76.47058823529412, 'classifier_40': 86.27450980392157}
# graph = {40: 86.27450980392157, 50: 88.23529411764706, 20: 70.58823529411765, 10: 70.58823529411765, 30: 76.47058823529412}

# graph = {50: 92.85714285714286}
def create_graph(testing_file,nb):
    graph_accur,graph_false,graph_missplaced,graph_missed = create_datas(testing_file,nb)

    print(graph_accur)
    print(graph_false)
    print(graph_missplaced)
    print(graph_missed)
    xlabel = 'percent of the file'
    ylabel = 'accuracy'
    fig1 = plt.figure(1)
    fig1.canvas.set_window_title('Accuracy')
    show_graph(graph_accur,'Accuracy',xlabel,ylabel)
    fig2 = plt.figure(2)
    fig2.canvas.set_window_title('False Alerts')
    show_graph(graph_false,'False Alerts',xlabel,ylabel)
    fig3 = plt.figure(3)
    fig3.canvas.set_window_title('Missplaced Alerts')
    show_graph(graph_missplaced,'Missplaced Alerts',xlabel,ylabel)
    fig4 = plt.figure(4)
    fig4.canvas.set_window_title('Missed Alerts')
    show_graph(graph_missed,'Missed Alerts',xlabel,ylabel)
    plt.show()
    
# create_graph(file_name)



# retrainnig problem
# emoticons
# time consuming for training testing


    
# print(os.listdir('../csv_files'))



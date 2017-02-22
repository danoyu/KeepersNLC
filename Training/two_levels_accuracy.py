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
import os
import matplotlib.pyplot as plt
from accuracies import accuracy

file_bad = "../csv_files/ownDB_good_level_of_bad.csv"  # name of the file with all the good-bad examples 
file_0_1 = "../csv_files/2ls_ownDB.csv"  # name of the file with all the bad examples

classifier_0_1 = 'classifier_0_1'
classifier_bad = 'classifier_bad'

file_name = "../csv_files/ownDB_good_level_of_bad.csv"

# training_0_1 = '../training_csv_files/training_0_1'
# training_bad = '../training_csv_files/training_bad'

# create 2 classifiers :
# 1 to class 0 or 1
# 2 to class 1,2,3 levels of bad
# with a file with 4 classes

#############
# demander si lors de l'apprentissage il faut prendre les meme phrases
# create a list of classifiers
def create_list_classifiers_2ls(filename):
    # 0.05 only 2 records not enough to train
    files = os.listdir('../training_csv_files')
    filename = filename.split('/')
    filename = filename[len(filename) - 1]
    filename = filename.split('.')[0]
    print(filename)
    for file in files:
        if file.__contains__(filename+'_bad') or file.__contains__(filename+'_0_1'):
            nb = file.split('_')
            nb = nb[len(nb) - 1]
            nb = nb.split('.')[0]
            name_classifier = file.split('.csv')[0] + '_classifier_' + nb
            classifier.create_classifier('../training_csv_files/' + file, name_classifier,nb)

# classifier.delete_by_id_classifiers()
# #create_list_classifiers_2ls(file_name)
# print(classifier.list_classifiers_name_id())
# print(len(classifier.list_classifiers_name_id()))
# def create2ls_list_classifiers(file_name):
# print classifiers with names
# print(classifier.list_classifiers_name_id())

#give accuracies with the two levels solution
def accuracy2(testing_file, classifier_name, classifier_bad):

    with open(testing_file) as csvfile:
            n_row = 0
            counter = 0
            counter_get_2 = 0 
            reader = csv.reader(csvfile)
            false_alerts_counter = 0  # number of predictions is 1,2 or 3 and the actual class is 0
            missplaced_alerts_counter = 0  # number of 
            missed_alerts_counter = 0  # number of predictions is 0 and the actual class is 1,2 or 3
            A = 0  # All that the prediction is different of 0
            T_1_2_3 = 0
            T_0 = 0
            # star process 
            for row in reader:
                    n_row += 1  # number of examples into the file 
                    actual_sentence = row[0]  # string of the example
                    actual_class = row[1]  # example that we already know  the class
                    print('O 1 classifier name :' ,classifier_name)                       
                    answer_class = classifier.classify(classifier_name, actual_sentence)  # classified class with more confidence 
                   
                    if answer_class == '1':
                        counter_get_2 += 1
                        # API CALL TO THE LEVEL-CLASSIFIER 
                        answer_class = classifier.classify(classifier_bad, actual_sentence)
                        print('bad classifier name :' ,classifier_bad) 
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
                        print(actual_class,answer_class)
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
            
    return accuracy, false_alerts, missplaced_alerts, missed_alert


# give the accuracies of all the classifiers for the testing_file
# return a dictionnary with the classifier and his one_level_accuracy
def test(testing_file, nb):
    classifiers = classifier.list_classifiers_name_id()
    accuracies = list()
    data = dict()
    classifier_0_1 = ''
    classifier_bad = ''
    for num in nb:
        for classifi in classifiers:
            if(classifi.__contains__(str(num))):
                if(classifi.__contains__('0_1')):
                    classifier_0_1 = classifi
                if(classifi.__contains__('bad_' + str(num))):
                    classifier_bad = classifi
        print(num)
        print(classifier_0_1)
        print(classifier_bad)
        accur = accuracy(testing_file, classifier_0_1, classifier_bad)
        accuracies.append(accur)
        data[num] = accur
        print(accur)
    print (data)
    return data

# nb = [30,40,50]
# print(test(file_name,nb))

# create a graph with data
def create_graph_with_data(data):
    graph = dict()
    for name in data:
        p = int(name.split('classifier_')[1])
        graph[p] = data[name]
    return graph
    

# data = {'classifier_10': 70, 'classifier_20': 77, 'classifier_30': 80}
# create_graph_with_data(data)

# data = {'classifier_50': 88.23529411764706, 'classifier_10': 70.58823529411765, 'classifier_20': 70.58823529411765, 'classifier_30': 76.47058823529412, 'classifier_40': 86.27450980392157}
# graph = {40: 86.27450980392157, 50: 88.23529411764706, 20: 70.58823529411765, 10: 70.58823529411765, 30: 76.47058823529412}


def create_graph(testing_file, nb):
    graph = test(testing_file, nb)
    print(graph)
    plt.xlabel('percent of DB')
    plt.ylabel('two_level_accuracy')
    plt.plot(*zip(*sorted(graph.items())))
    plt.show()
    
# create_graph(file_name,nb)

def create_datas(testing_file, nb):
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
                if(classifi.__contains__('0_1')):
                    classifier_0_1 = classifi
                if(classifi.__contains__('bad_' + str(num))):
                    classifier_bad = classifi
        print(num)
        print(classifier_0_1)
        print(classifier_bad)
        accur, false_alerts, missplaced_alerts, missed_alert = accuracy2(testing_file, classifier_0_1, classifier_bad)
        accuracies.append(accur)
        missplaced.append(missplaced_alerts)
        missed.append(missed_alert)
        false.append(false_alerts)
        data_accur[num] = accur
        data_false[num] = false_alerts
        data_missplaced[num] = missplaced_alerts
        data_missed[num] = missed_alert
    return data_accur, data_false, data_missplaced, data_missed

# print(create_datas(file_name))
 
def show_graphs(graph, title, xlabel, ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(*zip(*sorted(graph.items())))
    
# data = {'classifier_10': 70, 'classifier_20': 77, 'classifier_30': 80}
# create_graph_with_data(data)

# data = {'classifier_50': 88.23529411764706, 'classifier_10': 70.58823529411765, 'classifier_20': 70.58823529411765, 'classifier_30': 76.47058823529412, 'classifier_40': 86.27450980392157}
# graph = {40: 86.27450980392157, 50: 88.23529411764706, 20: 70.58823529411765, 10: 70.58823529411765, 30: 76.47058823529412}

# graph = {50: 92.85714285714286}
def create_graphs(testing_file, nb):
    data_accur, data_false, data_missplaced, data_missed = create_datas(testing_file, nb)
    print(data_accur)
    print(data_false)
    print(data_missplaced)
    print(data_missed)
    xlabel = 'percent of the file'
    ylabel = 'accuracy'
    fig1 = plt.figure(1)
    fig1.canvas.set_window_title('Accuracy')
    show_graphs(data_accur, 'Accuracy', xlabel, ylabel)
    fig2 = plt.figure(2)
    fig2.canvas.set_window_title('False Alerts')
    show_graphs(data_false, 'False Alerts', xlabel, ylabel)
    fig3 = plt.figure(3)
    fig3.canvas.set_window_title('Missplaced Alerts')
    show_graphs(data_missplaced, 'Missplaced Alerts', xlabel, ylabel)
    fig4 = plt.figure(4)
    fig4.canvas.set_window_title('Missed Alerts')
    show_graphs(data_missed, 'Missed Alerts', xlabel, ylabel)
    plt.show()

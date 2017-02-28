'''
Created on Feb 12, 2017

@author: Dan
'''
import training
import classifier
import one_level_accuracy
import os
from classifier import delete_by_id_classifiers, list_classifiers_name_id
import two_levels_accuracy
import matplotlib.pyplot as plt

filename = '../csv_files/ownDB_good_level_of_bad.csv'
nb = [10, 15, 20, 25, 30, 35, 45, 40, 50, 60, 70, 65]

def exe_1_level(file_name, nb):
    print(filename)
    print(nb)
    classifier.delete_by_id_classifiers()
    training.create_training_files(file_name, nb)
    classifier.create_list_classifiers(file_name)
    print(classifier.list_classifiers_name_id())
    one_level_accuracy.create_graph(file_name,nb)

# print(classifier.list_classifiers_name_id())
# classifier.delete_by_id_classifiers()
exe_1_level(filename, nb)  

def exe_2_levels(file_name, nb):
    # print(filename)
    # print(nb)
    classifier.delete_by_id_classifiers()
    training.create_training_files_0_1_and_bad(file_name, nb)
    two_levels_accuracy.create_list_classifiers_2ls(file_name)
    print(classifier.list_classifiers_name_id())
    two_levels_accuracy.create_graphs(file_name, nb)

# exe_2_levels(filename,nb)  

def show_graphs(graph1, graph2, title, xlabel, ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(*zip(*sorted(graph1.items())), label='one_level')
    plt.plot(*zip(*sorted(graph2.items())), label='two_level')
    plt.legend(loc=2)
    
 
def one_graphs(testing_file, nb):
    print(filename)
    print(nb)
    
    classifier.delete_by_id_classifiers()
    training.create_training_files(testing_file, nb)
    classifier.create_list_classifiers(testing_file)
    data_accur, data_false, data_missplaced, data_missed = one_level_accuracy.create_datas(testing_file, nb)
    
    classifier.delete_by_id_classifiers()
    training.create_training_files_0_1_and_bad(testing_file, nb)
    two_levels_accuracy.create_list_classifiers_2ls(testing_file)
    data_accur2, data_false2, data_missplaced2, data_missed2 = two_levels_accuracy.create_datas(testing_file, nb)
    
    xlabel = 'percent of the data'
    ylabel = 'accuracy'
    fig1 = plt.figure(1)
    fig1.canvas.set_window_title('Accuracy')
    show_graphs(data_accur, data_accur2, 'Accuracy', xlabel, ylabel)
    fig2 = plt.figure(2)
    fig2.canvas.set_window_title('False Alerts')
    show_graphs(data_false, data_false2, 'False Alerts', xlabel, ylabel)
    fig3 = plt.figure(3)
    fig3.canvas.set_window_title('Missplaced Alerts')
    show_graphs(data_missplaced, data_missplaced2, 'Missplaced Alerts', xlabel, ylabel)
    fig4 = plt.figure(4)
    fig4.canvas.set_window_title('Missed Alerts')
    show_graphs(data_missed, data_missed2, 'Missed Alerts', xlabel, ylabel)
    plt.show()
    
# one_graphs(filename,nb) 

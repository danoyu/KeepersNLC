'''
Created on Feb 7, 2017

@author: חנן ליפסקין
'''


import csv
import linecache
import random
from mpmath import rand
import os
from argcomplete.compat import str



file = "../csv_files/ownDB_good_level_of_bad.csv"
target_file = "../training_csv_files/training_"

# select a training set that take random rows from a csv file
def select_training_sentences_random(file,p):
    # problem to use dialog api because of the name of the PC that is in hebrew
    # filename = askopenfile('.')
    f = open(file, 'r')
    
    # number of the line in the source file
    numline = len(f.readlines())
    f.close()
    
    # p percent of the number of the lines in the source file
    b = int(numline * p)
    
    # the training set with b entry
    set = list()
    
    # list of the index of the selected rows in the source file
    numbers = list()
    
    # take b line from the source file and make a set with b entry
    while b > 0 :
        # pick a random number to select a line
        rand = random.randint(1, numline)
        # select the random line
        row = (linecache.getline(file, rand).strip('\n'))
        # take only the line that are not in the set already
        if not(numbers.__contains__(rand)):
            r = row.split(',')
            # fix the comma problem
            # if a comma is in a sentences
            while not(r[1].isnumeric()):
                r[0] += r[1]
                r[1] = r[2]
                r.pop(2)
            numbers.append(rand)
            set.append(r) 
            # print (r)
            b -= 1
    return set
    
# print (select_training_sentences_random(0.5))

# create a csv file with the rows that selected by select_training_sentences_random(p)
def create_training_file_random(file,p, target_file):
    set = select_training_sentences_random(file,p)
    # print (len(set))
    # create a new file and put all the set on it line by line
    with open(target_file, 'w' , newline='') as f:
        writer = csv.writer(f)
        for i in range(len(set)):
            writer.writerow(set[i])
      
        
# create_training_file_random(0.3,target_file)

# select a training set that have 50% of several levels of bad(1,2,3) and 50% good(0)
# if the source file have an impair number of row it take one more of good 
def select_training_sentences_balance_good_bad(file,p):
    # problem to use dialog api because of the name of the PC that is in hebrew
    # filename = askopenfile('.')
    
    f = open(file, 'r')
    
    # number of the line in the source file
    numline = len(f.readlines())
    f.close()
    
    # p percent of the number of the lines in the source file
    b = int(numline * p)
    balance = int(b / 2)
    
    # the training set with b entry
    set = list()
    
    # list of the index of the selected rows in the source file
    numbers = list()
    numbers_good = list()
    numbers_bad = list()
    
    fix = 0
    if b % 2 != 0:
        fix = 1
    
    # take b line from the source file and make a set with b entry
    while b > 0 :
        # pick a random number to select a line
        rand = random.randint(1, numline)
        # select the random line
        row = (linecache.getline(file, rand).strip('\n'))
        # take only the line that are not in the set already
        if not(numbers.__contains__(rand)):
            r = row.split(',')
            
            # fix the comma problem
            # if a comma is in a sentences
            while not(r[1].isnumeric()):
                r[0] += r[1]
                r[1] = r[2]
                r.pop(2)
            r[1] = int(r[1])
    
            # if b if impair it take one more good
            if r[1] == 0 and len(numbers_good) < balance + fix:
                
                numbers_good.append(rand)
                numbers.append(rand)
                set.append(r) 
                # print (r)
                b -= 1
                
            if r[1] != 0 and len(numbers_bad) < balance :
                numbers_bad.append(rand)
                numbers.append(rand)
                set.append(r) 
                b -= 1
    
    return set
    
#print (select_training_sentences_balance_good_bad('../csv_files/ownDB_good_level_of_bad_BAD.csv',0.5))

# create a csv file with the rows that selected by select_training_sentences_random(p)
def create_training_file_balance_good_bad(source,p, target_file):
    set = select_training_sentences_balance_good_bad(source,p)
    # print (len(set))
    # create a new file and put all the set on it line by line
    with open(target_file, 'w' , newline='') as f:
        writer = csv.writer(f)
        for i in range(len(set)):
            writer.writerow(set[i])
        
#create_training_file_balance_good_bad(0.5, target_file+'0_1.csv')

# read a csv file and return a list of the good and a list of the bad sentences 
def extract_good_and_bad(file):
    
    # problem to use dialog api because of the name of the PC that is in hebrew
    # filename = askopenfile('.')
    list_good = list()
    list_bad = list()
    nb_lines = 0
    
    with open(file, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            nb_lines += 1
            # fix the comma problem
            # if a comma is in a sentences
            r = row
            while not(r[1].isnumeric()):
                r[0] += r[1]
                r[1] = r[2]
                r.pop(2)
            r[1] = int(r[1])
            if r[1] == 0 :
                list_good.append(r[0])
            else :
                list_bad.append(r[0])
    
    return list_good, list_bad, nb_lines

#print(extract_good_and_bad())

#create a file with just 2 classes based on the source file
def create_file_0_1(source,target):
    list_good, list_bad, nb_lines = extract_good_and_bad(source)
    with open(target, 'w',newline='') as t :
        writer = csv.writer(t)
        for good in list_good:
            writer.writerow([good,0])
        for bad in list_bad:
            writer.writerow([bad,1])
            
#create_file_0_1(file, target_file + 'q.csv')
      
def create_file_bad(source,target):
    with open(source,'rt') as f, open(target,'w',newline='') as t:
        reader = csv.reader(f)
        writer = csv.writer(t)
        for row in reader:
            if row[1] != '0':
                writer.writerow(row)
            
#create_file_bad(file, target_file+ 'q.csv')  


        
def pick_percent_list(liste, nb_pick):

    index = list()
    set = list()
    
    for i in range(nb_pick):
         # pick a random number to select a line
        rand = random.randint(0, len(liste) - 1)
        # select the random line
        # take only the line that are not in the set already
        if not(index.__contains__(rand)):
            index.append(rand)
            set.append(liste[rand]) 
            # print (liste[rand])
    return index, set
      
# prendre un certan pourcentage des bad et des good       
def select_training_file_balance_good_level_of_bad2(p, p_bad):
    list_good, list_bad, nb_lines = extract_good_and_bad()
    
    nb_good = len(list_good)
    nb_bad = len(list_bad)
    
    b = int(nb_lines * p) 
    b_good = int(nb_good)
    b_bad = int(nb_bad * p_bad)
    
    if b % 2 != 0:
        b_bad += 1
    
    set = list()
    print (b)
    print (b_good)
    print (b_bad)
    index = list()
    
    index_good, set_good = pick_percent_list(list_good, b_good)
    index_bad, set_bad = pick_percent_list(list_bad, b_bad)
    
    set.append(set_good)
    set.append(set_bad)
    
    index.append(index_good)
    index.append(index_bad)
    
    # print(set)
    return set
        
# select_training_file_balance_good_level_of_bad2(0.6,1,1)

def create_training_file_balance_good_level_of_bad2(p, target_file):
    set = ()  # select_training_file_balance_good_level_of_bad2(p)
    # print (len(set))
    # create a new file and put all the set on it line by line
    with open(target_file, 'w' , newline='') as f:
        writer = csv.writer(f)
        for i in range(len(set)):
            writer.writerow(set[i])



# create len(nb) training files based on file
def create_training_files(file,nb):
    # 0.05
    name = file.split('.csv')[0]
    name = name.split('/')
    name = name[len(name)-1]
    training = '../training_csv_files/' + name + '_'
    for i in nb:
        name = training + str(i) + '.csv'
        create_training_file_balance_good_bad(file,i / 100, name)
 
#nb = [10, 20, 30, 40, 50]       
#create_training_files(file,nb)
        

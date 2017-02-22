# give the accuracy of 1 classifier for the testing_file
def accuracy(testing_file, classifier_name):

    with open(testing_file) as csvfile:
            n_row = 0
            counter = 0
            reader = csv.reader(csvfile)
            false_alerts_counter = 0 #number of predictions is 1,2 or 3 and the actual class is 0
            missplaced_alerts_counter = 0 #number of 
            missed_alerts_counter = 0 #number of predictions is 0 and the actual class is 1,2 or 3
            A = 0 # All that the prediction is different of 0
            T_1_2_3 = 0
            # star process 
            for row in reader:
                    n_row += 1  # number of examples into the file 
                    actual_sentence = row[0]  # string of the example
                    actual_class = row[1]  # example that we already know  the class
                                                  
                    answer_class = classifier.classify(classifier_name, actual_sentence)  # classified class with more confidence 
                    print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                                #FINIR LE TEST D ACCURACY 
                    if actual_class == answer_class:  # asking for a hit
                        counter = counter + 1
                        #good prediction different of 0(missplaced_alert)
                        if actual_class != 0: 
                            missplaced_alerts_counter += 1  
                    #if the prediction is wrong        
                    else :
                        #when the class is 0 and the prediction is different of 0(false alert)
                        if actual_class == 0:
                            false_alerts_counter += 1
                        #when the actual class is 1,2 or 3 and it predict 0
                        if answer_class == 0: #else is ok too i think need to see 
                            missed_alerts_counter += 1
            
                    #when the prediction is different of 0
                    if answer_class != 0:
                        A += 1
                    if answer_class == 0:
                        T_0 += 1
                    
            accuracy = (counter / n_row) * 100
            false_alerts = false_alerts_counter / A
            missplaced_alerts = (A - missplaced_alerts_counter)/A
            T_1_2_3 = n_row - T_0
            missed_alert = missed_alerts_counter/T_1_2_3
            
            
            print("Results: ", "\n" , "Number of examples: ", n_row, "\n", "Number of hits: ", counter, '\n', "Accuracy: ", accuracy, "%",'\n', "False Alerts: ", false_alerts, "%",'\n', "Missplaced Alerts: ", missplaced_alerts, "%",'\n', "Missed Alerts: ", missed_alert, "%");   
            
    return accuracy

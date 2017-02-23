from flask import Flask
import os
import oneClick

app = Flask(__name__)

port = int(os.getenv('VCAP_APP_PORT'))

filename = '../csv_files/ownDB_good_level_of_bad.csv'
nb = [10, 15, 20, 25, 30, 35, 45, 40, 50, 60, 70, 65]

@app.route('/')
def hello_wolrd():
	oneClick.exe_1_level(filename,nb)
	list = classifier.list_classifiers_name_id()
	print (list)
	#return 'Hello ' + list
	return 'Hello world' + str(port)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
    
  
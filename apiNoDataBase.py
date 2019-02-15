
######################## INIT #########################
from flask import Flask
from flask import request
app = Flask(__name__)

database = []

###################### REQUESTS #######################

# POST
@app.route('/book/', methods=['POST'])
def Post():
	return '200: OK' + ' ' + str(request.data)

# GET
@app.route('/books/', methods=['GET'])
def Get():
	return '200: OK'

#################### AUX FUNCTIONS ####################
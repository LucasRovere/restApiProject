
######################## INIT #########################
from flask import Flask
from flask import request
from flask import json
from flask import make_response

app = Flask(__name__)

database = []

###################### REQUESTS #######################

# POST
@app.route('/book/', methods=['POST'])
def Post():
	resource = json.loads(request.data)

	# Verifica os dados obrigatórios
	if ('title' not in resource):
		return GenResponse(00, "Missing title")
	if ('isbn' not in resource):
		return GenResponse(400, "Missing isbn")

	# Tenta adicionar no banco de dados
	if (AddToDataBase(resource) == 1):
		return GenResponse(201, "Resource Added!")
	else:
		return GenResponse(400, "Unknown Error")

# GET
@app.route('/books/', methods=['GET'])
def Get():
	return '200: OK'

#################### AUX FUNCTIONS ####################

# Gera um arquivo do tipo response com os argumentos enviados
def GenResponse(code, type):
	the_response = make_response(type)
	the_response.status_code = code

	if(code == 201):
		the_response.headers["code"] = "Created"
	if(code == 204):
		the_response.headers["code"] = "No Content"
	if(code == 400):
		the_response.headers["code"] = "Bad Request"

	return the_response

# Adiciona novo recurso na memória
def AddToDataBase(data):
	try:
		database.append(data)
	except:
		return 0

	return 1

#the_response.code = "expired"
#the_response.error_type = "expired"
#the_response.status_code = 400
#the_response._content = b'{ "key" : "a" }'
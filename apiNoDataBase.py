
######################## INIT #########################
from flask import Flask
from flask import request
from flask import json
from flask import make_response

app = Flask(__name__)

database = []

###################### REQUESTS #######################

# POST
@app.route('/book', methods=['POST'])
def Post():
	resource = request.args.to_dict(True)

	if len(resource) == 0:
		resource = json.loads(request.data)

	# Verifica os dados obrigatórios
	if ('title' not in resource):
		return GenResponse(400, "Missing title", None)
	if ('isbn' not in resource):
		return GenResponse(400, "Missing isbn", None)

	# Tenta adicionar no banco de dados
	if (AddToDataBase(resource) == 1):
		return GenResponse(201, "Resource Added!", None)
	else:
		return GenResponse(400, "Unknown Error", None)

# GET
@app.route('/books/<isbn>', methods=['GET'])
def Get(isbn):
	requestedISBN = isbn
	result = SearchDataBase(requestedISBN)

	print(isbn)

	if result == None:
		return GenResponse(404, "Book not in DataBase", None)
	else:
		return GenResponse(200, "Book Found!", result)



#################### AUX FUNCTIONS ####################

# Gera um arquivo do tipo response com os argumentos enviados >>> Metodo POST
def GenResponse(code, type, data):
	the_response = make_response(type)
	the_response.status_code = code

	the_response.headers["book"] = data

	if(code == 200):
		the_response.headers["code"] = "OK"
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

def SearchDataBase(isbn):
	for book in database:
		print("_" + str(book['isbn']) + "_" + str(isbn) + "_")
		if  int(isbn) == int(book['isbn']):
			return book

	return None

#the_response.code = "expired"
#the_response.error_type = "expired"
#the_response.status_code = 400
#the_response._content = b'{ "key" : "a" }'

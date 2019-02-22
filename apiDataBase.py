
######################## INIT #########################
from flask import Flask
from flask import request
from flask import json
from flask import make_response
from bs4 import BeautifulSoup
import requests
import re

from WebSearcher import WebSearcher
from DAO import DAO

database = []
hasSearchedKotlin = False

app = Flask(__name__)
dao = DAO()

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
		return GenResponse(500, "Unknown Error", None)

# GET
@app.route('/books/<isbn>', methods=['GET'])
def Get(isbn):
	CheckKotlinDB()
	result = dao.Get(isbn)

	return GenResponse(200, "", result)

@app.route('/books/', methods=['GET'])
def GetAll():
	CheckKotlinDB()
	result = dao.GetAll()
	
	return GenResponse(200, "", result)

#################### AUX FUNCTIONS ####################

def CheckKotlinDB():
	global hasSearchedKotlin

	# Variável global "hasSearchedKotlin" mostra se os livros encontrados
	# na página já foram buscados e adicionados na base de dados;
	# Evitando buscas desnecessárias
	if hasSearchedKotlin == True:
		return
	else:
		hasSearchedKotlin = True

	ws = WebSearcher()
	foundData = ws.SearchKotlinDB()
	dao.AddList(foundData)

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

# Descrição como string
def GetDescription(currentTag):
	try:
		currentTag = currentTag.next_sibling.next_sibling
		description = ""

		while currentTag.name == "p":
			description += currentTag.get_text()
			currentTag = currentTag.next_sibling.next_sibling		

		# Algumas descrições vem com caracteres que precisam ser removidos
		return description.encode('latin-1', 'ignore')

	except:
		return ""

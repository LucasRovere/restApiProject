
######################## INIT #########################
from flask import Flask
from flask import request
from flask import json
from flask import make_response

from bs4 import BeautifulSoup

import requests
import re

from DAO import DAO

database = []
hasSearchedKotlin = False

app = Flask(__name__)
dao = DAO()

###################### REQUESTS #######################

# POST
@app.route('/book', methods=['POST'])
def Post():
	# Converte os parâmetros url para um dicionário python
	resource = request.args.to_dict(True)

	# Caso os parâmetros não estejam na url, procura no corpo do request
	if len(resource) == 0:
		resource = json.loads(request.data)

	# Verifica os dados obrigatórios
	if ('title' not in resource):
		return GenResponse(400, "Missing title", None)
	if ('isbn' not in resource):
		return GenResponse(400, "Missing isbn", None)

	# Tenta adicionar no banco de dados
	if (dao.AddSingle(resource)):
		return GenResponse(201, "Resource Added!", None)
	else:
		return GenResponse(500, "Unknown Error", None)

# GET
@app.route('/books/<isbn>', methods=['GET'])
def Get(isbn):
	result = dao.Get(isbn)
	return GenResponse(200, "", result)

# GET ALL
@app.route('/books/', methods=['GET'])
def GetAll():
	result = dao.GetAll()
	return GenResponse(200, "", result)

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
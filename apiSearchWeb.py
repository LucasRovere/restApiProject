
######################## INIT #########################
from flask import Flask
from flask import request
from flask import json
from flask import make_response
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

database = []

# Falta:
# https://kotlinandroidbook.com/

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

	if result == None:
		return GenResponse(404, "Book not in DataBase", None)
	else:
		return GenResponse(200, "Book Found!", result)

@app.route('/books/', methods=['GET'])
def GetAll():
	SearchKotlinDB()
	return GenResponse(404, "Book not in DataBase", None)

##################### WEB SEARCH ######################

# Busca os links do site kotlinlang
def SearchKotlinDB():
	kotlinPage = requests.get("https://kotlinlang.org/docs/books.html")

	if kotlinPage.status_code != 200:
		return None

	kotlinSoup = BeautifulSoup(kotlinPage.content, 'html.parser')

	# Os links e títulos de livros estão dentro da tag "article"
	article = kotlinSoup.find_all('article')[0];

	# Retorna todos os títulos de livros.
	# Formato para busca:
	# <h2> Título
	# <div class="book-lang"> Idioma
	# <a href=url> Imagem
	# <p> <a>Título<\a> Descrição
	# *<p> Descrição adicional*
	# <h2> Próximo livro
	bookList = article.find_all("h2")
	isbnList = []

	for titleTag in bookList:
		langTag = titleTag.next_sibling.next_sibling
		imageTag = langTag.next_sibling.next_sibling
		url = imageTag['href']

		print("\tSearch at " + url)

		urlIsbn = SearchIsbnAt(url)
		print("Found isbn = " + str(urlIsbn))

def SearchIsbnAt(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
	cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
	bookPage = requests.get(url, headers=headers, cookies=cookies)
	bookSoup = BeautifulSoup(bookPage.content, 'html5lib')

	if "manning" in url:
		return GetIsbnManning(bookSoup)
	if "leanpub" in url:
		return -1
	if "packtpub" in url:
		return GetIsbnPacktpub(bookSoup)
	if "amazon" in url:
		return GetIsbnAmazon(bookSoup)
	if "fundamental-kotlin" in url:
		return GetIsbnFundamentalKotlin(bookSoup)
	if "kuramkitap" in url:
		return GetIsbnKuramkitap(bookSoup)
	if "raywenderlich" in url:
		return -1
	if "editions-eni" in url:
		return -1
	if "kotlinandroidbook" in url:
		return -1

	return -1

################### CASOS CONHECIDOS ##################
# table-row table-body-row prd_custom_fields_0
def GetIsbnManning(pageSoup):
	try:
		productInfo = pageSoup.find(class_="product-info")

		for tag in productInfo.find_all("li"):
			tagText = tag.get_text()
			if "ISBN" in tagText:
				return int(re.search(r'\d+', tagText).group())

		return -1
	except:
		return -1

def GetIsbnPacktpub(pageSoup):
	try:
		isbnString = pageSoup.find(itemprop="isbn").get_text()
		isbnInt = int(re.search(r'\d+', isbnString).group())
		return isbnInt
	except:
		return -1

def GetIsbnAmazon(pageSoup):
	try:
		productInfo = pageSoup.find("table", id="productDetailsTable")
		
		for tag in productInfo.find_all("li"):
			tagText = tag.get_text()
			if "ISBN-13" in tagText:
				tagText = tagText.replace("ISBN-13", "").replace("-", "")
				return int(re.search(r'\d+', tagText).group())

		return -1
	except:
		return -1

def GetIsbnFundamentalKotlin(pageSoup):
	try:
		productInfo = pageSoup.find(class_="scondary_content")

		for tag in productInfo.find_all("h2"):
			if "ISBN" in tag.get_text():
				return int(re.search(r'\d+', tag.get_text()).group())
	except:
		return -1

def GetIsbnKuramkitap(pageSoup):
	codeInfo = pageSoup.find(class_="table-row table-body-row prd_custom_fields_0")
	codeText = codeInfo.get_text()
	return int(re.search(r'\d+', codeText).group())

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

# Busca a base de dados local pelo código isbn
def SearchDataBase(isbn):
	for book in database:
		print("_" + str(book['isbn']) + "_" + str(isbn) + "_")
		if  int(isbn) == int(book['isbn']):
			return book

	return None
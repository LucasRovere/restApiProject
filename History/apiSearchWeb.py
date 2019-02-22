
######################## INIT #########################
from flask import Flask
from flask import request
from flask import json
from flask import make_response
from bs4 import BeautifulSoup
import requests
import re

database = []
hasSearchedKotlin = False

app = Flask(__name__)

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
	SearchKotlinDB()

	requestedISBN = isbn
	result = SearchDataBase(requestedISBN)

	return GenResponse(200, "", result)

@app.route('/books/', methods=['GET'])
def GetAll():
	SearchKotlinDB()
	
	return GenResponse(200, "", database)

##################### WEB SEARCH ######################

# Busca os links do site kotlinlang
def SearchKotlinDB():
	global hasSearchedKotlin

	# Variável global "hasSearchedKotlin" mostra se os livros encontrados
	# na página já foram buscados e adicionados na base de dados;
	# Evitando buscas desnecessárias
	if hasSearchedKotlin == True:
		return
	else:
		hasSearchedKotlin = True

	# Recupera o html da página do kotlin
	kotlinPage = requests.get("https://kotlinlang.org/docs/books.html")

	# Verifica se a página foi carregada com sucesso antes de continuar
	if kotlinPage.status_code != 200:
		return None

	# Converte o html em uma bela sopa para facilitar a navegação
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

	# Para cada tag de título encontrada (para cada livro)
	# encontra as informações no site e busca o isbn pelo link externo de compra
	for titleTag in bookList:
		# Encontra as informações seguindo a organização de tags mostrada acima
		langTag = titleTag.next_sibling.next_sibling
		imageTag = langTag.next_sibling.next_sibling

		url = imageTag['href']

		urlIsbn = SearchIsbnAt(url)
		descripton = GetDescription(imageTag)
		language = langTag.get_text()
		title = titleTag.get_text()

		if urlIsbn == -1:
			isbnString = "Unavailiable"
		else:
			isbnString = str(urlIsbn)

		data = {
			"title" : title,
			"descripton" : descripton,
			"language" : language,
			"isbn" : isbnString
		}

		AddToDataBase(data)

# Busca o isbn numa url
def SearchIsbnAt(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
	cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
	bookPage = requests.get(url, headers=headers, cookies=cookies)
	bookSoup = BeautifulSoup(bookPage.content, 'html5lib')

	print("Search at " + url)

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
	try:
		codeInfo = pageSoup.find(class_="table-row table-body-row prd_custom_fields_0")
		codeText = codeInfo.get_text()
		return int(re.search(r'\d+', codeText).group())
	except:
		return -1

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
		if  str(isbn) == str(book['isbn']):
			return book

	return None

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

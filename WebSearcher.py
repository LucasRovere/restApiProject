
from bs4 import BeautifulSoup
import sqlite3
import requests
import re

class WebSearcher:

	# Busca os links do site kotlinlang
	def SearchKotlinDB(self):
		# Informação
		print("Empty Database:\nSearching kotlinlang")

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

		foundData = []

		# Para cada tag de título encontrada (para cada livro)
		# encontra as informações no site e busca o isbn pelo link externo de compra
		for titleTag in bookList:
			# Encontra as informações seguindo a organização de tags mostrada acima
			langTag = titleTag.next_sibling.next_sibling
			imageTag = langTag.next_sibling.next_sibling

			url = imageTag['href']

			# Informação
			print("Searching [" + str(bookList.index(titleTag) + 1) + "/" + str(len(bookList)) + "]")
			print("\tURL: " + url)

			# Salva os dados encontrados dos livros em strings separadas
			urlIsbn = self.SearchIsbnAt(url)
			description = self.GetDescription(imageTag)
			language = langTag.get_text()
			title = titleTag.get_text()

			if urlIsbn == -1:
				isbnString = "Unavailiable"
			else:
				isbnString = str(urlIsbn)

			data = {
				"title" : title,
				"description" : description,
				"language" : language,
				"isbn" : isbnString
			}

			foundData.append(data)

		return foundData

	# Busca o isbn numa url
	def SearchIsbnAt(self, url):
		# Alguns sites da lista bloqueiam requisições sem headers com no mínimo dados de usuário e/ou cookies
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
		cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
		bookPage = requests.get(url, headers=headers, cookies=cookies)
		bookSoup = BeautifulSoup(bookPage.content, 'html5lib')

		# Verifica o site em questão para decidir o método apropriado para recuperar o isbn
		# Alguns sites não tem a informação do isbn por isso nem são verificados
		if "manning" in url:
			return self.GetIsbnManning(bookSoup)
		if "leanpub" in url:
			return -1
		if "packtpub" in url:
			return self.GetIsbnPacktpub(bookSoup)
		if "amazon" in url:
			return self.GetIsbnAmazon(bookSoup)
		if "fundamental-kotlin" in url:
			return self.GetIsbnFundamentalKotlin(bookSoup)
		if "kuramkitap" in url:
			return self.GetIsbnKuramkitap(bookSoup)
		if "raywenderlich" in url:
			return -1
		if "editions-eni" in url:
			return -1
		if "kotlinandroidbook" in url:
			return -1

		return -1

	# Descrição como string
	def GetDescription(self, currentTag):
		try:
			# Recupera a primeira tag <p> contendo descrição
			currentTag = currentTag.next_sibling.next_sibling
			description = ""

			# Alguns livros ustilizam mais de uma tag <p> em sequencia para a descrição.
			# Após todas as descrições a próxima tag será <h2> com o título do próximo livro.
			while currentTag.name == "p":
				description += currentTag.get_text()
				currentTag = currentTag.next_sibling.next_sibling		

			# Algumas descrições vem com caracteres que precisam ser removidos
			description = description.replace('\n', ' ').replace('\t', ' ')
			return description

		except:
			# Caso ocorra algum erro inesperado o default 'Unavailiable' será retornado
			return "Unavailiable"

################### CASOS CONHECIDOS ##################

	def GetIsbnManning(self, pageSoup):
		try:
			productInfo = pageSoup.find(class_="product-info")

			for tag in productInfo.find_all("li"):
				tagText = tag.get_text()
				if "ISBN" in tagText:
					return int(re.search(r'\d+', tagText).group())

			return -1
		except:
			return -1

	def GetIsbnPacktpub(self, pageSoup):
		try:
			isbnString = pageSoup.find(itemprop="isbn").get_text()
			isbnInt = int(re.search(r'\d+', isbnString).group())
			return isbnInt
		except:
			return -1

	def GetIsbnAmazon(self, pageSoup):
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

	def GetIsbnFundamentalKotlin(self, pageSoup):
		try:
			productInfo = pageSoup.find(class_="scondary_content")

			for tag in productInfo.find_all("h2"):
				if "ISBN" in tag.get_text():
					return int(re.search(r'\d+', tag.get_text()).group())
		except:
			return -1

	def GetIsbnKuramkitap(self, pageSoup):
		try:
			codeInfo = pageSoup.find(class_="table-row table-body-row prd_custom_fields_0")
			codeText = codeInfo.get_text()
			return int(re.search(r'\d+', codeText).group())
		except:
			return -1

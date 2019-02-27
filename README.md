Resumo:

	Projeto de uma API REST'com funções básicas;
	O projeto é feito por etapas, conforme novas funcionalidades são adicionadas
	O arquivo readme define qual é o arquivo com a versão mais completa e como utilizar a API
	Os arquivos antigos são mantidos no repositório como histórico de construção do projeto

Arquivos da versão atual:

	apiDataBase.py (Aplicativo Flask)
	WebSearcher.py (classe auxiliar; Vasculha https://kotlinlang.org/docs/books.html em busca dos dados dos livros)
	DAO.py (classe auxiliar; acesso à base de dados)

	Para rodar:	export FLASK_APP=apiDataBase.py
				flask run

Arquivo para testes:

	> requestTester.py
	> Testa todos os casos da api; mais explicações no arquivo
	> Basta rodar o arquivo no mesmo computador rodando o servidor
	> Caso nescessário a url deve ser alterada diretamente no script

	Para rodar:	python requestTester.py
	* Enquanto o aplicativo flask estiver rodando

Formato de dados dos livros JSON:

	> 'title': Título do livro
	> 'description': Descrição do livro
	> 'isbn': Código isbn associado ao livro; chave primária
	> 'language': Idioma do livro

Headers da resposta (objeto do tipo Response):

	> 'status_code': Código de status HTTP da resposta
	> 'code': Nome do erro associado ao código
	> 'book': Dados de livro no formato JSON associado à resposta no método GET

Métodos do arquivo atual:

	Método: POST
	> Descrição: Adiciona uma nova entidade de livro à base de dados, com as informações fornecidas; Recebe parâmetros pelo campo 'data' do request
	> Campos
		>> Url: '/book'
		>> data: Dados do livro em formato json como mostrado acima
	> Respostas:
		>> Sucesso:
			>> [201: Created] Quando o post adiciona um livro com sucesso na base de dados
		>> Erros:
			>> [400: Bad Request] Quando há parâmetros faltando no argumento do post ou algo de errado aconteceu

	Método: POST
	> Descrição: Adiciona uma nova entidade de livro à base de dados, com as informações fornecidas; Recebe parâmetros pela url
	> Campos
		>> Url: '/book?title=Book+title+example&description=Book+description+example&isbn=9999999999999&language=BR'
	> Respostas:
		>> Sucesso:
			>> [201: Created] Quando o post adiciona um livro com sucesso na base de dados
		>> Erros:
			>> [400: Bad Request] Quando há parâmetros faltando no argumento do post ou algo de errado aconteceu

	Método: GET
	> Descrição: Retorna as informações do livro com o isbn desejado
	> Url: '/books/{id}'
	> Sucesso:
		> [200: OK] Dados JSON encontrados no header 'book'

	Método: GET
	> Descrição: Retorna as informações de todos os livros na base de dados
	> Url: '/books/'
	> Sucesso:
		> [200: OK] Dados JSON encontrados no header 'book'

Base de Dados:

	A base de dados foi simulada através da biblioteca SQLite3 do python.
	Os dados ficam salvos em um arquivo 'book.db' no diretório do aplicativo.

Pacotes python instalados:

	> Flask
	> BeautifulSoup

Referências utilizadas:

	>> http://flask.pocoo.org/docs/1.0/quickstart/
	>> https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
	>> https://bocoup.com/blog/documenting-your-api
	>> https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree

Arquivos antigos:

	> helloWorld.py: É obrigatório programar um helloWorld quando se usa uma nova ferramente pela primeira vez
	> apiBasics.py: Arquivo de teste para realizar outras funções além de hello world; requests sem body
	> apiNoDataBase.py: Realiza POST e GET porém sem utilizar uma base de dados e sem buscar dados na web
	> apiSearchWeb.py: POST e GET, realizando busca na web para completar a base de dados

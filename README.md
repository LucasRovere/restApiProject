Resumo do projeto
	Projeto de uma API REST'com funções básicas;
	O projeto é feito por etapas, conforme novas funcionalidades são adicionadas
	O arquivo readme define qual é o arquivo com a versão mais completa e como utilizar a API
	Os arquivos antigos são mantidos no repositório como histórico de construção do projeto

Arquivo da versão atual:
	apiNoDataBase.py

Objetivo e detalhes da versão atual:
	Versão para testar o recebimento de parâmetros junto com o request.
	As informações serão adicionadas apenas à memória e as entidades adicionadas serão perdidas ao encerrar o processo.

Objetivos das versões futuras:
	Salvar em disco as informações adicionadas em disco para acesso;
	Acessar o site https://kotlinlang.org/docs/books.html para busca adicional de livros não presentes na base de dados;
	Adicionar os livros encontrados na web à base de dados do sistema;
	Outras funcionalidades podem ser adicionadas conforme eu tiver ideias;

Métodos do arquivo atual:
	> Método: POST
	> Descrição: Adiciona uma nova entidade de livro à base de dados, com as informações fornecidas
	> Url: '/book'
	> Sucesso:
	> Erros:

	> Método: GET
	> Descrição: Retorna as informações do livro com o ID desejado
	> Url: '/books/{id}'
	> Sucesso:
	> Erros:

Referências utilizadas:
	>> http://flask.pocoo.org/docs/1.0/quickstart/
	>> https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
	>> https://bocoup.com/blog/documenting-your-api

Arquivos antigos:
	> helloWorld.py: É obrigatório programar um helloWorld quando se usa uma nova ferramente pela primeira vez
	> apiBasics.py: Arquivo de teste para realizar outras funções além de hello world; requests sem body
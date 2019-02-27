
import requests

def main():
    # Testa o post enviando os dados pelo campo 'data'
    urlPost = 'http://127.0.0.1:5000/book'
    # Testa o post enviando os dados pela url
    urlPost2 = 'http://127.0.0.1:5000/book?title=Book+title+example&description=Book+description+example&isbn=9781617293291&language=BR'
    # Testa o get para o primeiro livro enviado (urlPost)
    urlGet = 'http://127.0.0.1:5000/books/9781617293290'
    # Testa o get para o segundo livro enviado (urlPost2)
    urlGet2 = 'http://127.0.0.1:5000/books/9781617293291'
    # Testa o get para um livro da base de dados do kotlin
    urlGet3 = 'http://127.0.0.1:5000/books/9788692030710'
    # Testa o get para todos os livros
    urlGet4 = 'http://127.0.0.1:5000/books/'

    # Dados do urlPost para serem enviados pelo campo data
    data ='''{
    "title": "Book title example",
    "description": "Book description example",
    "isbn": "9781617293290",
    "language": "BR"
    }'''

    response = requests.post(urlPost, data=data)
    print("Response POST 1:")
    print(response.content)

    response = requests.post(urlPost2)
    print("Response POST 2:")
    print(response.content)

    response = requests.get(urlGet)

    print("Response GET 1:")
    print(response.content)
    print("Resource Found:")
    print(response.headers['book'])

    response = requests.get(urlGet2)

    print("Response GET 2:")
    print(response.content)
    print("Resource Found:")
    print(response.headers['book'])

    response = requests.get(urlGet3)

    print("Response GET 3:")
    print(response.content)
    print("Resource Found:")
    print(response.headers['book'])

    response = requests.get(urlGet4)

    print("Response GET 4:")
    print(response.content)
    print("Resource Found:")
    print(response.headers['book'])

if __name__=='__main__':
    main()
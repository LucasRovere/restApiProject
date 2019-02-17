
import requests

def main():
    urlPost = 'http://127.0.0.1:5000/book'
    urlPost2 = 'http://127.0.0.1:5000/book?title=Book+title+example&description=Book+description+example&isbn=9781617293291&language=BR'
    urlGet = 'http://127.0.0.1:5000/books/9781617293290'
    urlGet2 = 'http://127.0.0.1:5000/books/9781617293291'

    data ='''{
    "title": "Book title example",
    "description": "Book description example",
    "isbn": "9781617293290",
    "language": "BR"
    }'''

    print("Posting")

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

if __name__=='__main__':
    main()
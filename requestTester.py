
import requests

def main():
    urlPost = 'http://127.0.0.1:5000/book/'
    urlGet = 'http://127.0.0.1:5000/books/9781617293290'

    data ='''{
    "title": "Book title example",
    "description": "Book description example",
    "isbn": "9781617293290",
    "language": "BR"
    }'''

    print("Posting")

    response = requests.post(urlPost, data=data)

    print("Response POST:")
    print(response.content)

    response = requests.get(urlGet)

    print("Response GET:")
    print(response.content)
    print("Resource Found:")
    print(response.headers['book'])

if __name__=='__main__':
    main()
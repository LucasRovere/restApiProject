
import requests

def main():
    url = 'http://127.0.0.1:5000/book/'

    data ='''{
    "title": "Book title example",
    "description": "Book description example",
    "isbn": "9781617293290",
    "language": "BR"
    }'''

    response = requests.post(url, data=data)

    print(response.content)


if __name__=='__main__':
    main()
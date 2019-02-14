from flask import Flask
app = Flask(__name__)

@app.route('/')
def Index():
    return 'Index'

@app.route('/book/')
def Post():
    return 'Post'

@app.route('/books/')
def Get():
    return 'Get'

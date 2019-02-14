from flask import Flask
app = Flask(__name__)


###################### REQUESTS ######################

# POST
@app.route('/book/')
def Post():
    return 'Post'

# GET
@app.route('/books/')
def Get():
    return 'Get'

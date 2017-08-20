import flask

app = flask.Flask(__name__)

@app.route('/greet/<username>')
def greet(username):
    import pymongo
    client = pymongo.MongoClient('mongo.taller', 27017)
    db = client['db']
    users = db['users']
    users.insert_one({ 'username' : username })
    return "Hello, " + users.find_one({ 'username' : username })['username']

if __name__ == '__main__':
    pass
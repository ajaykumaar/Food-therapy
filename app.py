from flask import *
import pymongo 
from pymongo import MongoClient

connection_url = 'mongodb+srv://ajaykumaar:ajay@cluster0.07d2o.mongodb.net/food-therapy?retryWrites=true&w=majority'
app=Flask(__name__)
client = pymongo.MongoClient(connection_url) 

Database = client.get_database('food-therapy') 
table = Database.confessions


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/lament', methods=['POST', 'GET'])
def lament():
    return render_template('form.html')

@app.route('/save', methods=['POST', 'GET'])
def save():
    name=request.form.get('name')
    confession=request.form.get('confession')
    tags=request.form.get('tags')

    table.insert_one({"Name":name, "Confession":confession, "Tags":tags})

    return render_template('blank.html')

if __name__ == "__main__":
    app.run(debug=True)
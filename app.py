from flask import *
import pymongo 
from pymongo import MongoClient
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

connection_url = 'mongodb+srv://ajaykumaar:ajay@cluster0.07d2o.mongodb.net/food-therapy?retryWrites=true&w=majority'
app=Flask(__name__)
client = pymongo.MongoClient(connection_url) 

Database = client.get_database('food-therapy') 
table = Database.confessions

def predict(model,tags):
  tag_l=[]
  tag_l.append(tags)
  max_len = 20 
  trunc_type = "post" 
  padding_type = "post" 

  file_path='static/tokenizer.sav'
  tokenizer=joblib.load(file_path)
  new_seq = tokenizer.texts_to_sequences(tag_l)
  padded = pad_sequences(new_seq, maxlen =max_len,
                      padding = padding_type,
                      truncating=trunc_type)
  return model.predict(padded)

def get_food(num):
    if num == 1:
        return ['Chocolates','Ice cream',' Sandwich']
    elif num == 2:
        return ['Biscuits','Fries','Chocolates']
    elif num == 3:
        return ['Pizza','Briyani','Noodles']
    elif num == 4:
        return ['Mac and Cheese','Fried chicken','Candy']
    elif num == 5:
        return ['Briyani','Ice cream','Chocolates']
    elif num == 6:
        return ['Coffee','Fruits','Hot chocolate']
    elif num == 7:
        return ['Briyani','Ice cream','Chocolates']
    elif num == 8:
        return ['Chocolates','Water','Paani poori']


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

    file_path='static/foodtherapy_model.sav'
    model=joblib.load(file_path)
    preds=predict(model,str(tags))
    foods=get_food(int(preds))

    table.insert_one({"Name":name, "Confession":confession, "Tags":tags})

    return render_template('food.html',foods=foods)

if __name__ == "__main__":
    app.run(debug=True)
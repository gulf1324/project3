from flask import Flask, Blueprint, render_template
from flask import request
import pickle
import locale 

with open(f'model/model.pkl','rb') as pickle_file:
    model = pickle.load(pickle_file)

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def main():
    
    if request.method == 'GET':
        return(render_template('index.html'))

    if request.method == 'POST':
        age = int(request.form['age'])
        height_cm = int(request.form['height_cm'])
        weight_kgs = int(request.form['weight_kgs'])
        body_type = int(request.form['body_type'])
        balance = int(request.form['balance'])
        overall_rating = int(request.form['overall_rating'])
        tags = int(request.form['tags'])
        skill_moves = int(request.form['skill_moves'])

        input_array = [[age,height_cm,weight_kgs,body_type,balance,overall_rating,tags,skill_moves]]

        prediction = model.predict(input_array)[0]


    return render_template('index.html',original_input={'나이':age,
                                                        '키':height_cm,
                                                        '몸무게':weight_kgs,
                                                        '체형':body_type,
                                                        '밸런스':balance,
                                                        '오버롤':overall_rating,
                                                        '태그':tags,
                                                        '개인기':skill_moves}, result= prediction)

    

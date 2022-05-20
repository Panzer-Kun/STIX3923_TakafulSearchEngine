from flask import Flask, jsonify, render_template
from flask import request

from TakafulSystem import System

app = Flask(__name__)

ts = System(debug=True)

@app.route('/search')
def home_page():
    query = request.args.get('q')
    model = request.args.get('model')
    
    if model is None:
       model = 'w2v'

    print('query : ' + query)
    print('model : ' + model)

    response = jsonify(ts.getAnswer(query, model))
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response




from flask import Flask, render_template
from flask import request

from TakafulSystem import System

app = Flask(__name__)

ts = System(debug=True)

@app.route('/search')
def home_page():
    query = request.args.get('q')
    print(query)
    return ts.getAnswer(query)




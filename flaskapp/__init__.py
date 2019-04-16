from flask import Flask
from flask import session, render_template, request
from datetime import datetime, date
from flask import g , Response, make_response, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True

app.jinja_env.trim_blocks = True


@app.route("/")
def helloworld():
    return "Hello Flask World!"

@app.route("/home_page")
def home_page():
    return render_template("home-page.html")

@app.route("/product_page")
def product_page():
    return render_template("product-page.html")

@app.route("/checkout_page")
def checkout_page():
    return render_template("checkout-page.html")

@app.route("/recording_modal")
def recording():
    return render_template('macro.html')


@app.route('/mongo', methods=['GET'])
def mongoTest():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.merchandise
    collection = db.user
    results = collection.find()
    client.close()
    return render_template('mongo.html', data=results)

 










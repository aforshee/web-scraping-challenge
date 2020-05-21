import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route('/scrape')
def scrapey():
    db = mongo.db.mars_db.mars
    data = scrape()
    # print(data)
    result = db.replace_one({}, data, upsert=True)
    # print(result.acknowledged, result.matched_count, result.modified_count)
    
    return redirect("http://localhost:5000/", code=302)

@app.route('/')
def index():
    mars_info = mongo.db.mars_db.mars.find_one()
    return render_template('index.html', **mars_info)
    # return render_template('index.html', info= mars_info)
if __name__ == "__main__":
    app.run(debug=True)
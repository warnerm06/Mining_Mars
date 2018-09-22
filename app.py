from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    

    return render_template("index.html")


@app.route("/scrape")
def scrape():
    news=scrape_mars.scrape_all()

    mongo.db.drop_collection('collection')

    mongo.db.collection.insert_one(news)
    
    data = mongo.db.collection.find_one() 

    return render_template("mars.html", data=data)


if __name__ == "__main__":
    app.run()

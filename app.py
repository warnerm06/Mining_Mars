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

    return render_template("mars.html", news=news)


if __name__ == "__main__":
    app.run()

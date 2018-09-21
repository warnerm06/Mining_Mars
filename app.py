from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    scraped_info=scrape_mars.scrape_all()

    return render_template("index.html",scraped_info=scraped_info)


@app.route("/scrape")
def scrape():
    return render_template("mars.html")


if __name__ == "__main__":
    app.run()

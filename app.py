import os
from flask import (
        Flask, flash, render_template, redirect, 
        request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html', page_title="Home page")


@app.route('/about')
def about():
    return render_template('about.html', page_title="About me & this page")


@app.route('/blog')
def post():
    blogposts = mongo.db.blog_posts.find()
    return render_template('blog.html', page_title="Blog posts", blogposts=blogposts)


@app.route('/contact')
def contact():
    return render_template('contact.html', page_title="Contact me")


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
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


@app.route("/")
def index():    
    return render_template("index.html", page_title="Home page")


@app.route("/blog")
def blog():
    blogposts = mongo.db.blog_posts.find()
    return render_template("blog.html", page_title="Blog posts", blogposts=blogposts)


@app.route("/postblog", methods=["GET", "POST"])
def postblog():
    if request.method == "POST":
        newblog = {
            "title": request.form.get("title"),
            "subtitle": request.form.get("subtitle"),
            "author": request.form.get("author"),
            "content": request.form.get("content")
        }

        mongo.db.blog_posts.insert(newblog)
        flash("Blog successfully posted!")
        return redirect(url_for("blog"))

    return render_template("postblog.html", page_title="Write a new blog!")


@app.route("/edit_blog/<blog_id>", methods=["GET", "POST"])
def edit_blog(blog_id):
    if request.method == "POST":
        blog = {
            "title": request.form.get("title"),
            "subtitle": request.form.get("subtitle"),
            "author": request.form.get("author"),
            "content": request.form.get("content")
        }
        mongo.db.blog_posts.update({"_id": ObjectId(blog_id)}, blog)
        flash("Blog Successfully Updated")

    blogpost = mongo.db.blog_posts.find_one({"_id": ObjectId(blog_id)})       
    return render_template("edit_blog.html", page_title="Edit Blog", blogpost=blogpost)


@app.route("/about")
def about():
    return render_template("about.html", page_title="About me & this page")


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact me")


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
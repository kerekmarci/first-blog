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
        return redirect(url_for("blog"))

    blogpost = mongo.db.blog_posts.find_one({"_id": ObjectId(blog_id)})       
    return render_template("edit_blog.html", page_title="Edit Blog", blogpost=blogpost)


@app.route("/delete_blog/<blog_id>")
def delete_blog(blog_id):
    mongo.db.blog_posts.remove({"_id": ObjectId(blog_id)})
    flash("Blog Successfully Deleted")
    return redirect(url_for("blog"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower() })

        if existing_user:
            flash("Username already exists. Try to log in")
            return redirect(url_for("login"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("blog", username=session["user"]))
    return render_template("register.html", page_title="Register a new account")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower() })
        
        if existing_user:
            # ensure hashed password matches input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome. {}".format(request.form.get("username")))
                    return redirect(url_for("blog"))
            else: 
                flash("Incorrect username or password")
                return redirect(url_for("login"))
        else:
            # username doesn't exist
            flash("Username doesn't exist")
            return redirect(url_for("login"))

    return render_template("login.html", page_title="Log in")


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
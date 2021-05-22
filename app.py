from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page_title="Home page")


@app.route('/about')
def about():
    return render_template('about.html', page_title="About me & this page")


@app.route('/post')
def post():
    return render_template('post.html', page_title="Blog posts")


@app.route('/contact')
def contact():
    return render_template('contact.html', page_title="Contact me")


if __name__ == '__main__':
    app.run(debug=True)
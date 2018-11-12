from flask import Flask, render_template
import datetime

app = Flask(__name__)
pages = ["Home","About","Contact","Projects"]

@app.route('/')
def home():
    return render_template("index.html", name=pages[0])

@app.route('/about/')
def about():
    return render_template("about.html", name=pages[1])

@app.route('/contact/')
def contact():
    return render_template("contact.html", name=pages[2])

@app.route('/projects/')
def projects():
    return render_template("projects.html", name=pages[3])

if __name__ == '__main__':
    app.run(debug=True)

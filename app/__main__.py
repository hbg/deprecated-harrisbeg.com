from flask import Flask, render_template
from flask_assets import Environment, Bundle

import datetime

app = Flask(__name__)
assets = Environment(app)

assets.url = app.static_url_path
assets.directory = app.static_folder
scss = Bundle('scss/about.scss', 'scss/projects.scss',"scss/contact.scss", filters='pyscss', output='all.css')
assets.register('scss_all', scss)

pages = ["Home","About","Contact","Projects"]
descriptions = ["A developer with no bounds, I have explored many languages and APIs, roamed through different jobs, and attempted to solve things myself for hours on end.", "About","Contact","Projects"]

@app.route('/')
def home():
    return render_template("index.html", name=pages[0], description=descriptions[0])

@app.route('/about/')
def about():
    return render_template("about.html", name=pages[1], description=descriptions[1])

@app.route('/contact/')
def contact():
    return render_template("contact.html", name=pages[2], description=descriptions[2])

@app.route('/projects/')
def projects():
    return render_template("projects.html", name=pages[3], description=descriptions[3])

if __name__ == '__main__':
    app.run(debug=True)

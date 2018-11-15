from flask import Flask, render_template, request
from flask_assets import Environment, Bundle
import datetime
import json
app = Flask(__name__)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('about.scss','404.scss', 'contact.scss', 'projects.scss',"index.scss", filters='pyscss', output='generated/all.css')

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
@app.route('/admin/')
def admin():
    return render_template("admin.html")
@app.route('/login', methods=['POST'])
def login():
        return("Success")

@app.route('/projects/<projectname>')
def projects_id(projectname):
    if (projectname == "UCSD"):
        desP = ["Center for Energy Research", "Cancer Center"]
        detail = ["At the Center of Energy, I attempted to find optimal computer vision settings (with OpenCV) for detecting the sun to aid the solar panels at UCSD.","At the Moores Cancer Research Center, I utilized my knowledge of data processing and Java to interpret genome files (.MAF)."]
        return render_template("project.html", name=projectname, titles=desP, details=detail)
    elif (projectname == "skinCAM"):
        desP = ["skinCAM"]
        detail = ["A child of my imagination, skinCAM, a patent-pending app, was created to allow for public access to dermatologic resources. By utilizing machine learning, skinCAM accurately detects many skin diseases - all for the price of, well, nil."]
        return render_template("project.html", name=projectname, titles=desP, details=detail)
    elif (projectname == "MSH"):
        desP = ["MySocialHub"]
        detail = ["A developer at MySocialHub, my primary job was frontend development for several sites including the famous salomondrin.com. These sites were all centered around one central platform, which primarily used the Laravel framework."]
        return render_template("project.html", name=projectname, titles=desP, details=detail)
    elif (projectname == "Grabify"):
        desP = ["Grabify"]
        detail = ["One of the most important sites I've worked on, Grabify is a security utility that allows one to log the IPs of others through the simple click of a link."]
        return render_template("project.html", name=projectname, titles=desP, details=detail)

@app.errorhandler(404)
def pagenotfound(e):
    return render_template("404.html", name="404", description="There's nothing to see here.")

if __name__ == '__main__':
    app.run(debug=True)

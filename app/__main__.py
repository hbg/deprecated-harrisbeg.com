from flask import Flask, render_template, request, redirect,url_for
from flask_assets import Environment, Bundle
import datetime
import requests
import json
app = Flask(__name__)
service = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
apiKey = "AIzaSyBilGD_-PomwT-XY1D6GlgQhs2rA-xX0uI"
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('about.scss','404.scss', 'contact.scss', 'projects.scss',"index.scss", filters='pyscss', output='generated/all.css')
token = ""
assets.register('scss_all', scss)

pages = ["Home","About","Contact","Projects"]
descriptions = ["A developer with no bounds, I have explored many languages and APIs, roamed through different jobs, and attempted to solve things myself for hours on end.", "About","Contact","Projects"]
def ulogin(em, pw):
    url = "%s?key=%s" % (service, apiKey)
    data = {"email": em,
            "password": pw,
            "returnSecureToken": True}
    result = requests.post(url, json=data)
    is_login_successful = result.ok
    json_result = result.json()
    token = json_result["idToken"][:9]
    print(token)
    if (("INVALID_PASSWORD") not in str(json_result)): # Crappy system but it'll do
        return json_result
    else:
        return "Error"
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

@app.route('/adminpanel/')
def adminpanel():
    email = request.args.get('email')
    id = request.args.get('id')
    return render_template("adminpanel.html", email=email, id=id)

@app.route('/login', methods=['POST'])
def login():
        yx = ulogin(request.form['email'], request.form['password'])
        if (yx != "Error"):
            return redirect("/adminpanel?email="+request.form['email']+"&id="+yx["idToken"][:9])
        else:
            return "nil"


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

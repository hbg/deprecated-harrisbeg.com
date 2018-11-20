from flask import Flask, render_template, request, redirect,url_for, make_response
from flask_assets import Environment, Bundle
import datetime
import requests
import json
import os
app = Flask(__name__)
service = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
apiKey = os.popen('heroku config:get APIKey').read()
app.config['SERVER_NAME'] = 'harris.com:5000'
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('design.scss','about.scss','404.scss', 'contact.scss', 'projects.scss',"index.scss", filters='pyscss', output='generated/all.css')
assets.register('scss_all', scss)

token = ""
jsonMD = {
        "design": {
            "titles": ["App Dev","TechnologiCoders","Linker","Mustafar","Royal Guard","Hypercharged"],
            "workdescriptions": ["The logo for the App Development club was conceived by me after thinking of how to combine the CCA Spirit colors, the symbol of the raven, and imagery that very clearly depicts the purpose of the club.", "While the primary objective of TechnologiCoders was to primarily focus on hardware, creating a website with a logo enforcing an image of creativity would likely attract more sponsors.", "An impromptu creation, 'Linker' was an app designed to link mobile phones to computers - a link very clearly seen in the logo itself.", "A planet in Star Wars hosting Darth Vader's own castle.","A royal guard from the Star Wars original trilogy.","Just like our content and quality, the Hypercharged logo is straight to the point and direct - both in styling and meaning."]

        },
        "Home": {
            "description": "A developer with no bounds, I have explored many languages and APIs, roamed through different jobs, and attempted to solve things myself for hours on end."
        },
        "About": {
            "description" : "About"
        },
        "Design": {
            "description" : "Design"
        },
        "Projects": {
            "description" : "Projects",
            "skinCAM": {
                "images" : ["sc_app_icon.png"]
            },
            "Grabify": {
                "images" : ["grabify.png"]
            },
            "MSH": {
                "images" : ["msh.png"]

            },
            "UCSD": {
                "images" : ["cer.png","mcc.png"]

            }
        }
        }


works = jsonMD["design"]['titles']
workdescriptions = jsonMD["design"]["workdescriptions"]
def ulogin(em, pw):
    url = "%s?key=%s" % (service, apiKey)
    data = {"email": em,
            "password": pw,
            "returnSecureToken": True}
    result = requests.post(url, json=data)
    is_login_successful = result.ok
    json_result = result.json()

    print(token)
    if (("INVALID_PASSWORD") not in str(json_result)): # Crappy system but it'll do
        return json_result
    else:
        return "Error"
@app.route('/')
def home():
    return render_template("index.html", name="Home", description=jsonMD["Home"]["description"])

@app.route('/about/')
def about():
    return render_template("about.html", name="About", description=jsonMD["About"]["description"])

@app.route('/postMessage/', methods=['POST'])
def postMessage():

    return request.form['messagePost']

@app.route('/design/')
def design():
    return render_template("design.html", name="Design", works=works,workdescriptions=workdescriptions,description=jsonMD["Design"]["description"])

@app.route('/projects/')
def projects():
    return render_template("projects.html", name="Projects", description=jsonMD["Projects"]["description"])
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

            req= make_response(redirect("/adminpanel?email="+request.form['email']+"&id="+yx["idToken"][:9]))
            #req.set_cookie('active', True)
            return req
        else:
            return "nil"


@app.route('/projects/<projectname>')
def projects_id(projectname):
    if (projectname == "UCSD"):
        desP = ["Center for Energy Research", "Cancer Center"]
        detail = ["At the Center of Energy, I attempted to find optimal computer vision settings (with OpenCV) for detecting the sun to aid the solar panels at UCSD.","At the Moores Cancer Research Center, I utilized my knowledge of data processing and Java to interpret genome files (.MAF)."]
        return render_template("project.html", name=projectname, titles=desP, details=detail, images=jsonMD["Projects"][projectname]["images"])
    elif (projectname == "skinCAM"):
        desP = ["skinCAM"]
        detail = ["A child of my imagination, skinCAM, a patent-pending app, was created to allow for public access to dermatologic resources. By utilizing machine learning, skinCAM accurately detects many skin diseases - all for the price of, well, nil."]
        return render_template("project.html", name=projectname, titles=desP, details=detail, images=jsonMD["Projects"][projectname]["images"])
    elif (projectname == "MSH"):
        desP = ["MySocialHub"]
        detail = ["A developer at MySocialHub, my primary job was frontend development for several sites including the famous salomondrin.com. These sites were all centered around one central platform, which primarily used the Laravel framework."]
        return render_template("project.html", name=projectname, titles=desP, details=detail, images=jsonMD["Projects"][projectname]["images"])
    elif (projectname == "Grabify"):
        desP = ["Grabify"]
        detail = ["One of the most important sites I've worked on, Grabify is a security utility that allows one to log the IPs of others through the simple click of a link."]
        return render_template("project.html", name=projectname, titles=desP, details=detail, images=jsonMD["Projects"][projectname]["images"])

@app.errorhandler(404)
def pagenotfound(e):
    return render_template("404.html", name="404", description="There's nothing to see here.")


if __name__ == '__main__':
    app.run(debug=True)

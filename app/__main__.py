from datetime import datetime, timezone
from typing import Type

import json
import os
import pyrebase  # Theoretically don't need this anymore
import requests
import uuid  # Or even this
from flask import Flask, render_template, request, redirect, make_response
from flask_assets import Environment
from flask_sitemap import Sitemap
from webassets import Bundle


class Reader:
    variables: Type[dict]

    def __init__(self, path):
        self.variables = dict()
        with open(path) as f:
            for line in f:
                key = line.split("=")[0].strip()
                value = line.split("=")[1].strip()
                self.variables.__setitem__(key, value)

    def get_keypair(self):
        return self.variables


app = Flask(__name__)
smp = Sitemap(app=app)
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
service = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
apiKey = os.environ.get('APIKey', None)
config = {
  "apiKey": apiKey,
  "authDomain": "adminhbeg.firebaseapp.com",
  "databaseURL": os.environ.get('databaseURL', None),
  "storageBucket": os.environ.get('storageBucket', None)
}
#
#   Purpose: If identified that this is a local env, use .gitignore file
#   
#   APIKey: Firebase authorization key
#
if apiKey is None:
    with open(r"app/static/js/config.json") as f:  # --> Use .env in the future
        config = json.load(f)
assets = Environment(app)
scss: Bundle = Bundle('design.scss', 'about.scss', '404.scss', '_main.scss', 'contact.scss', 'projects.scss', "index.scss", filters='pyscss', output='generated/all.css')
assets.register('scss_all', scss)
#
#   SCSS Compiled --> generated/all.css
#
token: Type[str]
email: Type[str]
message_blogs: Type[list]
date_blogs: Type[list]
title_stripped: Type[list]
title_blogs: Type[list]

with open("app/site_settings.json") as f:
    jsonMD = json.load(f)


firebase = pyrebase.initialize_app(config)
db = firebase.database()


def generateSpamToken():
    return uuid.uuid4()


def getDescription(page_name):
    return jsonMD[page_name]["description"]


def renderDB():
    message_blogs, date_blogs, title_blogs, title_stripped = [], [], [], []  # RESET DATA
    all_blogs = db.child("blogs").get()
    for user in all_blogs.each():
        #  Refreshes DB for new blog posts and such
        title_blogs.append(user.key())
        title_stripped.append(''.join(filter(str.isalnum, user.key())))
        date_blogs.append(user.val()["date"])
        message_blogs.append(user.val()["message"])
    return [message_blogs, date_blogs, title_blogs, title_stripped]

# SuperSpotter --> A Beta project tracking supercars


def user_login(email, password):
    url = "%s?key=%s" % (service, config["apiKey"])
    data = {"email": email,
            "password": password,
            "returnSecureToken": True}
    result = requests.post(url, json=data)
    json_result = result.json()
    if result.ok:  # Crappy system but it'll do
        return json_result
    else:
        return "Error"

r"""
@app.route('/superSpotter/')
def super_spotter():
    return render_template("superspotter.html", name="Super Spotter", description=getDescription("Home"))
"""

@app.route('/')
def home():
    #   I want to make a method for the code below, but have other important things to do
    return render_template("index.html", name="Home", description=getDescription("Home"))

"""
@app.route('/about/')
def about():
    return render_template("about.html", name="About", description=getDescription("About"))


@app.route('/postMessage/', methods=['POST'])
def post_message():
    if request.cookies.get('id'):
        # data to save
        db.child("blogs").child(request.form['titlePost']).set({
            "message": request.form['messagePost'],
            "date": datetime.now(timezone.utc).strftime("%m/%d/%Y"),
            "author": "Harris Beg"  # will change later
        }, token)
        #   db.blog.insert(request.form['messagePost'])
        return redirect("/#blogs")
    else:
        return render_template("admin.html", ERRORCODE="Session expired... please login again.")


@app.route('/design/')
def design():
    return render_template("design.html", name="Design", works=jsonMD["Design"]['titles'], workdescriptions=jsonMD["Design"]["workdescriptions"],description=getDescription("Design"))


@app.route('/projects/')
def projects():
    return render_template("projects.html", name="Projects", description=getDescription("Projects"))


@app.route('/admin/')
def admin():
    return render_template("admin.html")


@app.route('/adminpanel/')
def admin_panel():
    email = request.args.get('email')
    id = request.args.get('id')
    return render_template("adminpanel.html", email=email, id=id)


@app.route('/login', methods=['POST'])
def login():
        login_activity = user_login(request.form['email'], request.form['password'])
        print(str(login_activity))
        if login_activity != "Error":  # Pt.2 of crappy system, but it'll do
            token = login_activity["idToken"]
            req = make_response(redirect("/adminpanel?email="+request.form['email']+"&id="+token[:9]))
            if not request.cookies.get('id'):
                req.set_cookie('id', token, max_age=60)
            return req
        else:
            return render_template("admin.html",ERRORCODE="Invalid email or password.")


@app.route('/projects/<projectname>')
def projects_id(projectname):
    if projectname == "UCSD":
        desP = ["Center for Energy Research", "Cancer Center"]  # what is desP supposed to mean? idk
        detail = [
                  At the Center for Energy Research and the University of San Diego, California, I attempted to find optimal computer vision settings
                  (with OpenCV) for detecting the sun to aid the solar panels at UCSD. Much of this internship required optical and machine-learning-oriented knowledge.","At the Moores Cancer Research Center, I utilized my knowledge of data processing and Java to interpret genome files (.MAF). These mutation annotation format files, then, can be used to identify patterns in mutations within specific cancer types.
                  ]
        return render_template("project.html", name=projectname, titlesD=desP, details=detail, images=jsonMD["Projects"][projectname]["images"])
    elif projectname == "skinCAM":
        desP = ["skinCAM"]
        detail = [
            A child of my imagination, skinCAM, a patent-pending app, was created to allow for public access to dermatologic resources.
            By utilizing machine learning, skinCAM accurately detects many skin diseases - all for the price of, well, nil.
                 ]
        return render_template("project.html", name=projectname, titlesD=desP, details=detail, images=jsonMD["Projects"][projectname]["images"])
    elif projectname == "MSH":
        desP = ["MySocialHub"]
        detail = ["A developer at MySocialHub, my primary job was frontend development for several sites including the famous salomondrin.com. These sites were all centered around one central platform, which primarily used the Laravel framework. With the developers assigned to different tasks, I have garnered both frontend and backend web development experience from this job."]
        return render_template("project.html", name=projectname, titlesD=desP, details=detail, images=jsonMD["Projects"][projectname]["images"])
    elif projectname == "Grabify":
        desP = ["Grabify"]
        detail = ["One of the most important sites I've worked on, Grabify is a security utility that allows one to log the IPs of others through the simple click of a link. Grabify is currently ranked at the #36,000 spot nationally and has been featured on MTV's show, Catfish."]
        return render_template("project.html", name=projectname, titlesD=desP, details=detail, images=jsonMD["Projects"][projectname]["images"])


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", name="404", description="There's nothing to see here.")


"""
if __name__ == '__main__':
    if os.environ.get("TEST", None) is None:  # In case of Heroku & local
        app.run(debug=True)
    else:  # For Travis CI
        print("Build succeeded for TRAVIS CI")
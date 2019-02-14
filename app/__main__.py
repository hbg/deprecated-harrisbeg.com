from flask import Flask, render_template, request, redirect,url_for, make_response
from flask_assets import Environment, Bundle
from flask_sitemap import Sitemap
from datetime import datetime, timezone
import pyrebase, requests, json, os, uuid
app = Flask(__name__)
smp = Sitemap(app=app)
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS']=True
service = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
apiKey = os.environ.get('APIKey', None)
config = {
  "apiKey": apiKey,
  "authDomain": "adminhbeg.firebaseapp.com",
  "databaseURL": os.environ.get('databaseURL', None),
  "storageBucket": os.environ.get('storageBucket', None)
}
#   Purpose: If identified that this is a local env, use .gitignore'd file
#   
#   APIKey: Firebase authorization key
#
if (apiKey == None):
    with open(r"app/static/js/config.json") as f:
        config = json.load(f)
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('design.scss','about.scss','404.scss', '_main.scss','contact.scss', 'projects.scss',"index.scss", filters='pyscss', output='generated/all.css')
assets.register('scss_all', scss)
#
#   SCSS Compiled --> generated/all.css
#
global messageBlogs,dateBlogs,titleBlogs,titleStripped
token, email = "",""
#
#   Site 'structure' of sorts
#
jsonMD = {
        "design": {
            "titles": ["App Dev","TechnologiCoders","Linker","Mustafar","Royal Guard","Hypercharged"],
            "workdescriptions": ["The logo for the App Development club was conceived by myself after thinking of how to combine Canyon Crest Academy's Spirit colors, its very own Raven, and imagery that very clearly depicts the purpose of the club.", "While the primary objective of TechnologiCoders was to primarily focus on hardware, creating a website with a logo enforcing an image of creativity would likely attract more sponsors.", "An impromptu creation, 'Linker' was an app designed to link mobile phones to computers - a link very clearly seen in the logo itself.", "A planet in Star Wars hosting Darth Vader's own castle.","A royal guard from the Star Wars original trilogy.","Just like our content and quality, the Hypercharged logo is straight to the point and direct - both in styling and meaning."]

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
        "Blog": {
            "description" : "Blog"
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

#   Initialize Firebase DB (Will use MongoDB soon)

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#   Returns a token-identifier for the spam button... prevents automated bots from entering site

def generateSpamToken():
    return uuid.uuid4()

def renderDB():
    messageBlogs,dateBlogs,titleBlogs,titleStripped = [],[],[],[]
    all_blogs = db.child("blogs").get()
    for user in all_blogs.each():
        #  Refreshes DB for new blog posts and such
        titleBlogs.append(user.key())
        titleStripped.append(''.join(filter(str.isalnum, user.key())))
        dateBlogs.append(user.val()["date"])
        messageBlogs.append(user.val()["message"])
    return [messageBlogs, dateBlogs, titleBlogs, titleStripped]

# SuperSpotter --> A Beta project tracking supercars

@app.route('/superSpotter/')
def superSpotter():
    return  render_template("superspotter.html", name="Super Spotter", description=jsonMD["Home"]["description"], titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])

def ulogin(em, pw):
    url = "%s?key=%s" % (service, config["apiKey"])
    data = {"email": em,
            "password": pw,
            "returnSecureToken": True}
    result = requests.post(url, json=data)
    json_result = result.json()
    if (result.ok): # Crappy system but it'll do
        return json_result
    else:
        return "Error"

@app.route('/')
def home():
    #   I want to make a method for the code below, but have other important things to do
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return render_template("index.html", name="Home", description=jsonMD["Home"]["description"], titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])

@app.route('/about/')
def about():
    return render_template("about.html", name="About", description=jsonMD["About"]["description"], titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])

@app.route('/postMessage/', methods=['POST'])
def postMessage():
    if (request.cookies.get('id')):
        # data to save
        data = {
            "message": request.form['messagePost'],
            "date": datetime.now(timezone.utc).strftime("%m/%d/%Y"),
            "author": "Harris Beg"  #   will change later
        }
        results = db.child("blogs").child(request.form['titlePost']).set(data, token)
        #   db.blog.insert(request.form['messagePost'])
        return redirect("/#blogs")
    else:
        return render_template("admin.html",ERRORCODE="Session expired.")

@app.route('/design/')
def design():
    return render_template("design.html", name="Design", works=works,workdescriptions=workdescriptions,description=jsonMD["Design"]["description"], titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])

@app.route('/projects/')
def projects():
    return render_template("projects.html", name="Projects", description=jsonMD["Projects"]["description"], titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])

@app.route('/admin/')
def admin():
    return render_template("admin.html")

@app.route('/adminpanel/')
def adminpanel():
    email = request.args.get('email')
    id = request.args.get('id')
    return render_template("adminpanel.html", email=email, id=id, titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])

@app.route('/login', methods=['POST'])
def login():
        yx = ulogin(request.form['email'], request.form['password'])
        print(str(yx))
        if (yx != "Error"): #   Pt.2 of crappy system, but it'll do
            req= make_response(redirect("/adminpanel?email="+request.form['email']+"&id="+yx["idToken"][:9]))
            token = yx["idToken"]
            if not request.cookies.get('id'):
                req.set_cookie('id', token, max_age=60)
            return req
        else:
            return render_template("admin.html",ERRORCODE="Invalid email or password.")

@app.route('/projects/<projectname>')
def projects_id(projectname):
    if (projectname == "UCSD"):
        desP = ["Center for Energy Research", "Cancer Center"]
        detail = ["At the Center for Energy Research and the University of San Diego, California, I attempted to find optimal computer vision settings (with OpenCV) for detecting the sun to aid the solar panels at UCSD. Much of this internship required optical and machine-learning-oriented knowledge.","At the Moores Cancer Research Center, I utilized my knowledge of data processing and Java to interpret genome files (.MAF). These mutation annotation format files, then, can be used to identify patterns in mutations within specific cancer types."]
        return render_template("project.html", name=projectname, titlesD=desP, details=detail, images=jsonMD["Projects"][projectname]["images"], titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])
    elif (projectname == "skinCAM"):
        desP = ["skinCAM"]
        detail = ["A child of my imagination, skinCAM, a patent-pending app, was created to allow for public access to dermatologic resources. By utilizing machine learning, skinCAM accurately detects many skin diseases - all for the price of, well, nil."]
        return render_template("project.html", name=projectname, titlesD=desP, details=detail, images=jsonMD["Projects"][projectname]["images"], titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])
    elif (projectname == "MSH"):
        desP = ["MySocialHub"]
        detail = ["A developer at MySocialHub, my primary job was frontend development for several sites including the famous salomondrin.com. These sites were all centered around one central platform, which primarily used the Laravel framework. With the developers assigned to different tasks, I have garnered both frontend and backend web development experience from this job."]
        return render_template("project.html", name=projectname, titlesD=desP, details=detail, images=jsonMD["Projects"][projectname]["images"], titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])
    elif (projectname == "Grabify"):
        desP = ["Grabify"]
        detail = ["One of the most important sites I've worked on, Grabify is a security utility that allows one to log the IPs of others through the simple click of a link. Grabify is currently ranked at the #36,000 spot nationally and has been featured on MTV's show, Catfish."]
        return render_template("project.html", name=projectname, titlesD=desP, details=detail, images=jsonMD["Projects"][projectname]["images"], titles=renderDB()[2], strippedtitles=renderDB()[3], dates=renderDB()[1], messages=renderDB()[0])

@app.errorhandler(404)
def pagenotfound(e):
    return render_template("404.html", name="404", description="There's nothing to see here.")

if __name__ == '__main__':
    if (os.environ.get("TEST", None) == None):
        app.run(debug=True)
    else:
        print("Build succeeded for TRAVIS CI")

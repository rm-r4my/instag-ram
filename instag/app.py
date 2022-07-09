from flask import Flask, render_template, request, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:root@localhost:5432/db'
app.config['SECRET_KEY']= 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)



class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(90), unique=True, nullable=False)
    username = db.Column(db.String(90), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    isPhotographer = db.Column(db.Boolean, default=False, nullable=False)
    profileImageSrc = db.Column(db.String(80))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password







@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    elif request.method == 'POST':
        name = request.form['nm']
        emaill = request.form['email']
        passwd = request.form['passwd']
        if not name or not emaill or not passwd:
            return "<h1> erorr </h1>"
        else:
            if passwd == request.form['passw']:
                user = users(name, emaill, passwd)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                abort(404)
            






@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        userr = users.query.order_by(users.username).all()
        pasw = users.query.order_by(users.password).all()

        if request.form['nam'] == userr and request.form['pas'] == pasw: 
            return redirect(url_for("index"))
        else:
            abort(404)




'''
@app.route('/posts<nam1><nam2><tex>', methods=['GET', 'POST'])
def posts(nam1, nam2, tex):
    if request.method == "POST":
        tex = request.form['comment']
        return render_template("single-post.html", tex=tex, nam1=nam1, nam2=nam2)
    return render_template("single-post.html")
'''


@app.route('/posts', methods=['GET'])
def posts():
    return render_template("single-post.html")



@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        fil = request.files["image"]
        fil.save('static/image' + fil.filename)
        texxt = request.form['description']
        return redirect(url_for("posts", nam1=fil, nam2=texxt))
    else:
        return render_template("create-post.html")



@app.route('/')
def index():
    return render_template("index.html")





app.run()

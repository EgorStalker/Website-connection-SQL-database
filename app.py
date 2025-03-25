from flask import Flask, jsonify
from flask import request
from flask import render_template_string,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import  Mapped,mapped_column
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name_people: Mapped[str] = mapped_column(db.String(128), nullable=False)
    email: Mapped[str] = mapped_column(db.String(128), nullable=False)
    date: Mapped[str] = mapped_column(db.String(128), nullable=False)
    password: Mapped[str] = mapped_column(db.String(128), nullable=False)

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)



with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

def show_the_login_form():
    return render_template_string("""
        <form method="POST">
            <h3>Login</h3>
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Login"> 
        </form>
    """)


def do_the_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "username" and password == "password":
        return index()
    else:
        return "Invalid credentials. Please try again."


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


def show_the_registration():
    return render_template("register.html")


def do_the_registration():
    username = request.form.get('username')
    first_password = request.form.get('firstpassword')
    second_password = request.form.get('secondpassword')
    email = request.form.get('email')
    date = request.form.get('date')
    all_info = username,first_password,second_password,email,date

    if first_password != second_password:
        return "Password aren't qwedev"

    existing_user = User.query.filter_by(email =email).first()
    if existing_user:
        return "Username already exists."
    new_user = User(
        name_people = request.form.get('username'),
        email = request.form.get("email"),
        date = request.form.get('date'),
        password = request.form.get('firstpassword')
    )
    db.session.add(new_user)
    db.session.commit()
    return "Succseful"
@app.route("/register",methods=['GET',"POST"])
def registation():
    if request.method == "POST":
        return do_the_registration()
    else:
        return show_the_registration()

app.run(debug=True)

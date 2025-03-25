# from flask import Flask, render_template,request,render_template_string
# from markupsafe import escape
#
# app = Flask(__name__)
#
#
# @app.route('/')
# @app.route('/home')
# def index():
#     return render_template("index.html")
#
#
# @app.route('/about')
# def index_about():
#     return render_template("about.html")
#
#
# @app.route("/ageFilter/<age>")
# def about_us(age):
#     if int(escape(age)) > 18:
#         return "Bы можете зарегатся"
#
#     return "<h1>Bы ёще не готовы<h1/>"
#
# # @app.route("/login/<login>")
# # def login(login):
# #     if len(escape(login)) > 10:
# #         return "Укоротите пароль"
# #     elif len(escape(login))  <= 10 and len(escape(login)) != 0 :
# #         return "Логин подходить "
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f'Post {post_id}'
# # @app.route('/forum/<path:path>')
# # def forum
#
#
# def do_the_login():
#     return "Logging in with POST method."
#
# def show_the_login_form():
#     form = '''
#     <form method="POST">
#         Username: <input type="text" name="username"><br>
#         Password: <input type="password" name="password"><br>
#         <input type="submit" value="Login">
#     </form>
#     '''
#     return form
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()
# if __name__ == "__main__":
#     app.run(debug=True)

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

#
# @app.route('/books',methods=['GET'])
# def get_books():
#     books = Book.query.all()
#
#     books_data = [
#         {
#             'id':book.id,
#             'name_book' : book.name_book,
#             'year': book.year,
#             'page' : book.page,
#             'author_id' : book.author_id
#
#
#         }
#         for book in books
#     ]
#
#     return jsonify(books_data)
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")
# @app.route("/register",methods = ['GET',"POST"])
# def register():
#     return render_template("register.html")
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

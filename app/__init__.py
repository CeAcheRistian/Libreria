from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user
from flask_wtf.csrf import CSRFProtect

from werkzeug.exceptions import HTTPException



from .database import *

app = Flask(__name__)

csrf = CSRFProtect()

login_manager_app = LoginManager(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if User.query.filter(User.name == request.form['user']).first() == None:
            new_user = User(name=request.form['user'], password= User.password_encryption(request.form['password']), type_user='user')
            db.session.add(new_user)
            db.session.commit()
        else:
            return 'Usuario ya existente.'
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@login_manager_app.user_loader
def load_user(id):
    return User.get_user_by_id(id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        logged_user = User.authenticate(request.form['user'], request.form['password'])
        if logged_user:
            login_user(logged_user)

            if logged_user.type_user == 'admin':
                return redirect(url_for('index'))

            return redirect(url_for('index'))
            
        else:
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/new_books', methods=['GET', 'POST'])
def new_books():
    if request.method == 'POST':
        if request.form['names'] != '':
            author = Author(
                names = request.form['names'],
                last_names = request.form['last_names'],
                birth = request.form['birth']
            )
            db.session.add(author)
            db.session.commit()

        if request.form['isbn'] != '':
            new_book = Book(
                isbn = request.form['isbn'],
                title = request.form['title'],
                year = request.form['year'],
                price = request.form['price'],
                author_id = request.form['author_id']
            )
            db.session.add(new_book)
            db.session.commit()

        return render_template('new_book.html')
    else:
        return render_template('new_book.html')


@app.route('/list_books')
def list_books():
    books = Book.query.all()
    
    for book in books:
        print(book.author.names)
    return render_template('list_books.html', data=books)



def not_found(error):
    return render_template('errors/404.html'), 404


def init_app(config):
    app.register_error_handler(404, not_found)

    app.config.from_object(config)

    csrf.init_app(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

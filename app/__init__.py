from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect

from werkzeug.exceptions import HTTPException


from .database import *

app = Flask(__name__)

csrf = CSRFProtect()

login_manager_app = LoginManager(app)


@app.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.type_user == 'admin':
            sales = []
            data = {
                'title': 'Libros vendidos',
                'sales': sales
            }
        else:
            purchase = []
            data = {
                'title': 'Mis compras',
                'purchase': purchase
            }

        return render_template('index.html', data=data)
    else:

        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        if User.query.filter(User.name == request.form['user']).first() == None:
            new_user = User(name=request.form['user'], password=User.password_encryption(
                request.form['password']), type_user='user')

            db.session.add(new_user)
            db.session.commit()

        else:
            flash('Usuario ya existente', 'warning')
            return redirect(url_for('signup'))

        return redirect(url_for('login'))
    else:
        return render_template('signup.html')


@login_manager_app.user_loader
def load_user(id):
    return User.get_user_by_id(id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        logged_user = User.authenticate(
            request.form['user'], request.form['password'])
        if logged_user:
            login_user(logged_user)
            flash('¡Bienvenido(a) a la Librería ~Para todos los bolsillos~', 'success')

            if logged_user.type_user == 'admin':
                return redirect(url_for('index'))

            return redirect(url_for('index'))

        else:
            flash('Usuario o Password incorrectos.', 'warning')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'success')

    return redirect(url_for('login'))


@app.route('/new_book', methods=['GET', 'POST'])
@login_required
def new_book():
    if request.method == 'POST':

        if request.form['names'] != '':
            author = Author(
                names=request.form['names'],
                last_names=request.form['last_names'],
                birth=request.form['birth']
            )
            db.session.add(author)
            db.session.commit()

        if request.form['isbn'] != '':
            new_book = Book(
                isbn=request.form['isbn'],
                title=request.form['title'],
                year=request.form['year'],
                price=request.form['price'],
                author_id=request.form['author_id']
            )
            db.session.add(new_book)
            db.session.commit()

        return render_template('new_book.html')

    else:
        return render_template('new_book.html')


@app.route('/update_book', methods=['GET', 'POST'])
@login_required
def update_book():
    if request.method == 'POST':
        book = Book.query.filter(Book.isbn == request.form['isbn']).first()

        try:
            if book:
                book.isbn = request.form['isbn'],
                book.title = request.form['title'],
                book.year = request.form['year'],
                book.price = request.form['price'],
                book.author_id = request.form['author_id']

                db.session.commit()
                flash('Libro actualizado', 'success')

            else:
                flash('Libro no encontrado', 'warning')
                return redirect(url_for('update_book'))

        except Exception as e:
            print(e)
            flash('No se pudo actualizar el libro', 'warning')

        return render_template('update_book.html')
    else:
        return render_template('update_book.html')


@app.route('/delete_book', methods=['GET','POST'])
@login_required
def delete_book():
    if request.method == 'POST':
        book = Book.query.filter(Book.isbn == request.form['isbn']).first()

        if book:
            db.session.delete(book)
            db.session.commit()
            flash('libro eliminado', 'success')
        else:
            flash('libro no encontrado', 'warning')

        return render_template('delete_book.html')
    else:
        return render_template('delete_book.html')

@app.route('/list_books')
@login_required
def list_books():
    books = Book.query.all()

    return render_template('list_books.html', data=books)


def not_found(error):
    return render_template('errors/404.html'), 404


def unauthorized(error):
    flash('Primero debes iniciar sesión', 'warning')
    return redirect(url_for('login')), 401


def init_app(config):
    app.register_error_handler(404, not_found)
    app.register_error_handler(401, unauthorized)

    app.config.from_object(config)

    csrf.init_app(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

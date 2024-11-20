from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

import uuid

from .database import *

from .email import purchase_confirmation


app = Flask(__name__)

csrf = CSRFProtect()

login_manager_app = LoginManager(app)

mail = Mail()

@app.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.type_user == 'admin':
            sales = Book.books_sold()
            data = {
                'title': 'Libros vendidos',
                'sales': sales
            }
        else:
            purchases = Purchase.users_purchase(current_user)
            data = {
                'title': 'Mis compras',
                'purchases': purchases
            }
        return render_template('index.html', data=data)

    else:
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            if User.query.filter(User.name == request.form['user']).first() == None:
                new_user = User(name=request.form['user'], password=User.password_encryption(
                    request.form['password']), type_user='user')

                db.session.add(new_user)
                db.session.commit()

            else:
                flash('Usuario ya existente', 'warning')
                return redirect(url_for('signup'))

            return redirect(url_for('login'))
        except Exception as ex:
            return render_template('errors/error.html', message=format(ex))
    else:
        return render_template('signup.html')


@login_manager_app.user_loader
def load_user(id):
    return User.get_user_by_id(id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
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

        except Exception as ex:
            return render_template('errors/error.html', message=format(ex))
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
        try:
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
        
        except Exception as ex:
            return render_template('errors/error.html', message=format(ex))
    else:
        return render_template('new_book.html')


@app.route('/update_book', methods=['GET', 'POST'])
@login_required
def update_book():
    if request.method == 'POST':
        try:
            book = Book.query.filter(Book.isbn == request.form['isbn']).first()

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

        except Exception as ex:
            return render_template('errors/error.html', message=format(ex))

        return render_template('update_book.html')
    else:
        return render_template('update_book.html')


@app.route('/delete_book', methods=['GET','POST'])
@login_required
def delete_book():
    if request.method == 'POST':
        try:
            book = Book.query.filter(Book.isbn == request.form['isbn']).first()

            if book:
                db.session.delete(book)
                db.session.commit()
                flash('libro eliminado', 'success')
            else:
                flash('libro no encontrado', 'warning')

            return render_template('delete_book.html')
        except Exception as ex:
            return render_template('errors/error.html', message=format(ex))
    else:
        return render_template('delete_book.html')

@app.route('/list_books')
@login_required
def list_books():
    try:
        books = Book.query.all()

        data = {
            'title': 'Listado de libros',
            'books': books
        }
        return render_template('list_books.html', data=data)
    except Exception as ex:
            return render_template('errors/error.html', message=format(ex))
    

@app.route('/purchase_book', methods=['POST'])
@login_required
def purchase_book():
    data_request = request.get_json()
    data = {}
    try:
        purchase = Purchase(
            uuid = uuid.uuid4(),
            book_id = data_request['isbn'],
            user_id = current_user.id
        )
        db.session.add(purchase)
        db.session.commit()

        data['success'] = True

        purchase_confirmation(app, mail, current_user, purchase)
    except Exception as ex:
        data['success'] = False
        data['message'] = f'{ex}'
        raise ex

    return jsonify(data)


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

    mail.init_app(app)

    return app

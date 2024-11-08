from flask import Flask, render_template, request, redirect, url_for

from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

csrf = CSRFProtect()

db = SQLAlchemy()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['password'] == '123456':
            return redirect(url_for('index'))
        else:
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


def not_found(error):
    return render_template('errors/404.html'), 404


def init_app(config):
    app.config.from_object(config)
    app.register_error_handler(404, not_found)

    csrf.init_app(app)

    db.init_app(app)
    return app

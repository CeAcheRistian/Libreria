from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

def not_found(error):
    return render_template('errors/404.html'), 404

def init_app(config):
    app.config.from_object(config)
    app.register_error_handler(404, not_found)
    return app
from app import init_app

from config import config

configuration = config['development']

app = init_app(config=configuration)

if __name__ == "__main__":
    app.run()
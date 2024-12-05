from flask import Flask
from routes.router import router

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    with app.app_context():
        app.register_blueprint(router)
    return app
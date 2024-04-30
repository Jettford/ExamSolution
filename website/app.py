import os

import flask_profiler
from flask import Flask

from config import config
from filters import register_filters

app = Flask(
    __name__,
    template_folder=os.path.abspath(config.data_path + "templates/"),
    static_folder=os.path.abspath(config.data_path + "static/"),
    static_url_path=""
)

app.secret_key = config.get("SECRET_KEY")

with app.app_context():
    from routes.public import public
    app.register_blueprint(public)
    
    from routes.auth import auth
    app.register_blueprint(auth)
    
    from routes.booking import booking
    app.register_blueprint(booking, url_prefix="/bookings")
    
    from routes.lessons import lessons
    app.register_blueprint(lessons, url_prefix="/lessons")
    
    app.config["flask_profiler"] = {
        "enabled": config.get("DEBUG"),
        "storage": {
            "engine": "sqlalchemy",
            "db_url": "sqlite:///profiler.db"
        },
        "basicAuth":{
            "enabled": True,
            "username": "admin",
            "password": "admin"
        },
        "ignore": [
            "^/static/.*"
        ]
    }

    flask_profiler.init_app(app)

    register_filters(app)
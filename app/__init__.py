from pathlib import Path

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///workout.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # noqa: F401
    from app.routes import api

    app.register_blueprint(api)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"errors": error.messages}), 400

    @app.get("/")
    def index():
        return jsonify({"message": "Workout API is running"})

    return app

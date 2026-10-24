from pathlib import Path

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///workout.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Flask-SQLAlchemy stores this SQLite database in Flask's instance folder.
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.get("/")
    def index():
        return jsonify({"message": "Workout API is running"})

    return app

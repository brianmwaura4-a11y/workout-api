# Workout Application Backend

A Flask REST API for creating workouts and reusable exercises. Trainers can attach exercises to workouts and record sets, reps, or duration for each workout entry.

## Requirements

- Python 3.12.14
- Pipenv

This project uses the Python version recorded in `.python-version` because the lab's pinned Werkzeug version is incompatible with Python 3.14.

## Installation and database setup

Run these commands from the project directory:

```bash
pipenv install
FLASK_APP=run.py pipenv run flask db upgrade
pipenv run python seed.py
```

The migration files are included in `migrations/`, so a fresh clone should run `flask db upgrade`. Run `flask db init` only if you are creating a new migration repository from scratch.

The seed script adds example workouts, exercises, and workout exercise entries. It is safe to run again; it does not delete existing records.

## Run the API

```bash
FLASK_APP=run.py FLASK_DEBUG=1 pipenv run flask run
```

The local API will be available at `http://127.0.0.1:5000`. Keep the terminal running while making requests. In another terminal, you can check the welcome route:

```bash
curl http://127.0.0.1:5000/
```

## API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Return the API welcome message. |
| GET | `/workouts` | List all workouts with their exercises and targets. |
| POST | `/workouts` | Create a workout. |
| GET | `/workouts/<workout_id>` | Return one workout with its exercises and targets. |
| DELETE | `/workouts/<workout_id>` | Delete a workout and its exercise entries. |
| POST | `/workouts/<workout_id>/exercises` | Attach an existing exercise to a workout with targets. |
| GET | `/exercises` | List all reusable exercises. |
| POST | `/exercises` | Create an exercise. |
| GET | `/exercises/<exercise_id>` | Return one exercise. |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise and its workout entries. |

### Create a workout

```bash
curl -i -X POST http://127.0.0.1:5000/workouts \
  -H "Content-Type: application/json" \
  -d '{"name":"Upper Body","notes":"Strength session"}'
```

The `date` field is optional and defaults to today. `notes` is optional.

### Create an exercise

```bash
curl -i -X POST http://127.0.0.1:5000/exercises \
  -H "Content-Type: application/json" \
  -d '{"name":"Push-up","description":"Bodyweight horizontal press"}'
```

### Add an exercise to a workout

Use the workout and exercise IDs returned by the create requests. Include at least one positive integer target: `sets`, `reps`, or `duration_seconds`.

```bash
curl -i -X POST http://127.0.0.1:5000/workouts/1/exercises \
  -H "Content-Type: application/json" \
  -d '{"exercise_id":1,"sets":3,"reps":10}'
```

## Validation and data rules

- Workout and exercise names are required, trimmed, limited to 80 characters, and unique.
- Workout notes may contain up to 500 characters; exercise descriptions may contain up to 300 characters.
- Sets, reps, and duration must be positive integers.
- Every workout exercise entry must include at least one target.
- A workout cannot contain the same exercise more than once.
- Marshmallow schemas validate request data. Model validations and database constraints provide additional checks.
- Invalid requests return `400`; missing resources return `404`; duplicate names or assignments return `409`.

## Project structure

- `app/__init__.py` — Flask application factory, database setup, blueprint registration, and validation error handling
- `app/models.py` — Workout, Exercise, and WorkoutExercise models, relationships, validations, and constraints
- `app/schemas.py` — Marshmallow request validation and response serialization
- `app/routes.py` — API endpoints
- `migrations/` — Alembic migration history managed by Flask-Migrate
- `seed.py` — Example data for all models
- `run.py` — Flask application entry point
- `Pipfile` and `Pipfile.lock` — Dependency declarations and locked versions

## Running tests

Install the project dependencies, including development dependencies:

```bash
pipenv install --dev
```

Run the automated tests:

```bash
pipenv run python -m pytest -q
```

The tests use a temporary in-memory database, so they do not change your workout data.

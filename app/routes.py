from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Exercise, Workout, WorkoutExercise
from app.schemas import (
    ExerciseInputSchema,
    ExerciseOutputSchema,
    WorkoutExerciseInputSchema,
    WorkoutInputSchema,
    WorkoutOutputSchema,
)


api = Blueprint("api", __name__)

workout_input = WorkoutInputSchema()
workout_output = WorkoutOutputSchema()
exercise_input = ExerciseInputSchema()
exercise_output = ExerciseOutputSchema()
workout_exercise_input = WorkoutExerciseInputSchema()


def get_json_object():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        raise ValidationError(
            {"_schema": ["The request body must be a JSON object."]}
        )
    return body


@api.get("/workouts")
def list_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return jsonify(workout_output.dump(workouts, many=True))


@api.post("/workouts")
def create_workout():
    data = workout_input.load(get_json_object())
    workout = Workout(**data)
    db.session.add(workout)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A workout with that name already exists."}), 409

    return jsonify(workout_output.dump(workout)), 201


@api.get("/workouts/<int:workout_id>")
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    return jsonify(workout_output.dump(workout))


@api.delete("/workouts/<int:workout_id>")
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    db.session.delete(workout)
    db.session.commit()
    return "", 204


@api.get("/exercises")
def list_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercise_output.dump(exercises, many=True))


@api.post("/exercises")
def create_exercise():
    data = exercise_input.load(get_json_object())
    exercise = Exercise(**data)
    db.session.add(exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An exercise with that name already exists."}), 409

    return jsonify(exercise_output.dump(exercise)), 201


@api.get("/exercises/<int:exercise_id>")
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    return jsonify(exercise_output.dump(exercise))


@api.delete("/exercises/<int:exercise_id>")
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    db.session.delete(exercise)
    db.session.commit()
    return "", 204


@api.post("/workouts/<int:workout_id>/exercises")
def add_exercise_to_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return jsonify({"error": "Workout not found."}), 404

    data = workout_exercise_input.load(get_json_object())

    exercise = db.session.get(Exercise, data["exercise_id"])
    if exercise is None:
        return jsonify({"error": "Exercise not found."}), 404

    workout_exercise = WorkoutExercise(
        workout=workout,
        exercise=exercise,
        sets=data.get("sets"),
        reps=data.get("reps"),
        duration_seconds=data.get("duration_seconds"),
    )
    db.session.add(workout_exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            {"error": "That exercise is already in this workout."}
        ), 409

    return jsonify(workout_output.dump(workout)), 201

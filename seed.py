from datetime import date, timedelta

from app import create_app, db
from app.models import Exercise, Workout, WorkoutExercise


def find_or_create(model, name, **extra_fields):
    item = model.query.filter_by(name=name).first()
    if item is None:
        item = model(name=name, **extra_fields)
        db.session.add(item)
        db.session.flush()
    return item


def add_workout_exercise(workout, exercise, **targets):
    existing = WorkoutExercise.query.filter_by(
        workout_id=workout.id,
        exercise_id=exercise.id,
    ).first()

    if existing is None:
        db.session.add(
            WorkoutExercise(
                workout=workout,
                exercise=exercise,
                **targets,
            )
        )


def seed():
    app = create_app()

    with app.app_context():
        strength = find_or_create(
            Workout,
            "Full Body Strength",
            date=date.today(),
            notes="Foundational strength session",
        )
        conditioning = find_or_create(
            Workout,
            "Conditioning Circuit",
            date=date.today() + timedelta(days=1),
        )

        squat = find_or_create(
            Exercise,
            "Goblet Squat",
            description="Squat while holding a dumbbell at chest height",
        )
        pushup = find_or_create(
            Exercise,
            "Push-up",
            description="Bodyweight horizontal press",
        )
        plank = find_or_create(
            Exercise,
            "Plank",
            description="Hold a straight body position",
        )

        add_workout_exercise(strength, squat, sets=3, reps=10)
        add_workout_exercise(strength, pushup, sets=3, reps=12)
        add_workout_exercise(conditioning, plank, sets=3, duration_seconds=45)

        db.session.commit()
        print("Example workouts, exercises, and workout entries are ready.")


if __name__ == "__main__":
    seed()

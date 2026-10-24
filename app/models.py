from datetime import date

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

from app import db


class Workout(db.Model):
    __tablename__ = "workouts"
    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) BETWEEN 1 AND 80",
            name="ck_workouts_name_length",
        ),
        CheckConstraint(
            "notes IS NULL OR length(notes) <= 500",
            name="ck_workouts_notes_length",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.String(500))

    exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )

    @validates("name")
    def validate_name(self, _key, value):
        if not isinstance(value, str):
            raise ValueError("Workout name must be text.")
        value = value.strip()
        if not value or len(value) > 80:
            raise ValueError("Workout name must be 1 to 80 characters.")
        return value

    @validates("notes")
    def validate_notes(self, _key, value):
        if value is not None and len(value) > 500:
            raise ValueError("Workout notes cannot exceed 500 characters.")
        return value


class Exercise(db.Model):
    __tablename__ = "exercises"
    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) BETWEEN 1 AND 80",
            name="ck_exercises_name_length",
        ),
        CheckConstraint(
            "description IS NULL OR length(description) <= 300",
            name="ck_exercises_description_length",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(300))

    workout_links = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )

    @validates("name")
    def validate_name(self, _key, value):
        if not isinstance(value, str):
            raise ValueError("Exercise name must be text.")
        value = value.strip()
        if not value or len(value) > 80:
            raise ValueError("Exercise name must be 1 to 80 characters.")
        return value

    @validates("description")
    def validate_description(self, _key, value):
        if value is not None and len(value) > 300:
            raise ValueError("Exercise description cannot exceed 300 characters.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="uq_workout_exercise",
        ),
        CheckConstraint("sets IS NULL OR sets > 0", name="ck_positive_sets"),
        CheckConstraint("reps IS NULL OR reps > 0", name="ck_positive_reps"),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="ck_positive_duration",
        ),
        CheckConstraint(
            "sets IS NOT NULL OR reps IS NOT NULL OR duration_seconds IS NOT NULL",
            name="ck_workout_exercise_has_target",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False,
    )
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
    )
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="exercises")
    exercise = db.relationship("Exercise", back_populates="workout_links")

    @validates("sets", "reps", "duration_seconds")
    def validate_positive_target(self, key, value):
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool) or value <= 0
        ):
            raise ValueError(f"{key} must be a positive integer.")
        return value

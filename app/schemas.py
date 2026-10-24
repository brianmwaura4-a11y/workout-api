from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates,
    validates_schema,
)


class WorkoutInputSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=80),
    )
    date = fields.Date(required=False)
    notes = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=500),
    )

    @validates("name")
    def name_must_not_be_blank(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Name cannot be blank or whitespace only.")


class ExerciseInputSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=80),
    )
    description = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=300),
    )

    @validates("name")
    def name_must_not_be_blank(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Name cannot be blank or whitespace only.")


class WorkoutExerciseInputSchema(Schema):
    exercise_id = fields.Integer(
        required=True,
        strict=True,
        validate=validate.Range(min=1),
    )
    sets = fields.Integer(
        required=False,
        allow_none=True,
        strict=True,
        validate=validate.Range(min=1),
    )
    reps = fields.Integer(
        required=False,
        allow_none=True,
        strict=True,
        validate=validate.Range(min=1),
    )
    duration_seconds = fields.Integer(
        required=False,
        allow_none=True,
        strict=True,
        validate=validate.Range(min=1),
    )

    @validates_schema
    def require_at_least_one_target(self, data, **kwargs):
        target_fields = ("sets", "reps", "duration_seconds")
        if all(data.get(field) is None for field in target_fields):
            raise ValidationError(
                {"_schema": ["Provide sets, reps, or duration_seconds."]}
            )


class ExerciseOutputSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String(allow_none=True)


class WorkoutExerciseOutputSchema(Schema):
    exercise = fields.Nested(ExerciseOutputSchema)
    sets = fields.Integer(allow_none=True)
    reps = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)


class WorkoutOutputSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    date = fields.Date(format="%Y-%m-%d")
    notes = fields.String(allow_none=True)
    exercises = fields.Nested(WorkoutExerciseOutputSchema, many=True)

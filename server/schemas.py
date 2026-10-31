from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)

    @validates('name')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError('Name cannot be blank.')


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def require_reps_or_duration(self, data, **kwargs):
        if data.get('reps') is None and data.get('duration_seconds') is None:
            raise ValidationError('Provide either reps or duration_seconds.')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=1000))
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


class WorkoutListSchema(Schema):
    """Slim version of a workout for list views (no nested exercises)."""
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.Str()


class ExerciseDetailSchema(ExerciseSchema):
    """An exercise plus the workouts it appears in."""
    workouts = fields.List(fields.Nested(WorkoutListSchema), dump_only=True)

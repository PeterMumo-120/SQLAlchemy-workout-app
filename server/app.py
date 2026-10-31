from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema, ExerciseDetailSchema, WorkoutSchema,
    WorkoutListSchema, WorkoutExerciseSchema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutListSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


def error(message, status):
    return jsonify({'error': message}), status


def save(obj):
    """Add and commit an object; return an error response tuple on failure."""
    try:
        db.session.add(obj)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return error(f'Database constraint failed: {e.orig}', 400)
    return None


@app.route('/')
def index():
    return jsonify({'message': 'Workout API is running'})


# ---------- Workouts ----------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    return jsonify(workouts_schema.dump(Workout.query.all())), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found', 404)
    return jsonify(workout_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
        workout = Workout(**data)
    except ValidationError as e:
        return error(e.messages, 400)
    except ValueError as e:
        return error(str(e), 400)

    failure = save(workout)
    if failure:
        return failure
    return jsonify(workout_schema.dump(workout)), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found', 404)
    db.session.delete(workout)  # cascade removes its WorkoutExercises
    db.session.commit()
    return jsonify({'message': f'Workout {id} deleted'}), 200


# ---------- Exercises ----------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    return jsonify(exercises_schema.dump(Exercise.query.all())), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error('Exercise not found', 404)
    return jsonify(exercise_detail_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
        exercise = Exercise(**data)
    except ValidationError as e:
        return error(e.messages, 400)
    except ValueError as e:
        return error(str(e), 400)

    failure = save(exercise)
    if failure:
        return failure
    return jsonify(exercise_schema.dump(exercise)), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error('Exercise not found', 404)
    db.session.delete(exercise)  # cascade removes its WorkoutExercises
    db.session.commit()
    return jsonify({'message': f'Exercise {id} deleted'}), 200


# ---------- Adding an exercise to a workout ----------

@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST'],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return error('Workout not found', 404)
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return error('Exercise not found', 404)

    try:
        data = workout_exercise_schema.load(request.get_json() or {})
        link = WorkoutExercise(workout=workout, exercise=exercise, **data)
    except ValidationError as e:
        return error(e.messages, 400)
    except ValueError as e:
        return error(str(e), 400)

    failure = save(link)
    if failure:
        return failure
    return jsonify(workout_exercise_schema.dump(link)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)

# Workout Tracker API

## Description

A RESTful backend API for a workout tracking app used by personal trainers, built with Flask, SQLAlchemy, and Marshmallow. Trainers can create reusable exercises, log dated workouts, and add exercises to workouts with sets, reps, or duration.

Data integrity is enforced at three levels: database table constraints, SQLAlchemy model validations, and Marshmallow schema validations.

## Installation

Requires Python 3.8 or newer.

```bash
git clone https://github.com/PeterMumo-120/SQLAlchemy-workout-app.git
cd SQLAlchemy-workout-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd server
export FLASK_APP=app.py
flask db upgrade head
python3 seed.py
```

## Running the App

From the `server` folder:

```bash
flask run -p 5555
```

The API is available at http://127.0.0.1:5555

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /workouts | List all workouts |
| GET | /workouts/\<id> | Get one workout with its exercises, including reps, sets and duration |
| POST | /workouts | Create a workout (`date`, `duration_minutes`, optional `notes`) |
| DELETE | /workouts/\<id> | Delete a workout and its workout-exercise entries |
| GET | /exercises | List all exercises |
| GET | /exercises/\<id> | Get one exercise with the workouts it appears in |
| POST | /exercises | Create an exercise (`name`, `category`, optional `equipment_needed`) |
| DELETE | /exercises/\<id> | Delete an exercise and its workout-exercise entries |
| POST | /workouts/\<workout_id>/exercises/\<exercise_id>/workout_exercises | Add an exercise to a workout (`reps` and/or `duration_seconds`, optional `sets`) |
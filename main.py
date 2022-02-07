import os
import requests
import datetime as dt

# --------------------------------- PERSONAL CONFIG ---------------------------------
GENDER = "male"
WEIGHT_KG = 75
HEIGHT_CM = 180
AGE = 25

# ------------------------------ AUTHENTICATION CONFIG ------------------------------
API_EXERCISE = "https://trackapi.nutritionix.com/v2/natural/exercise"
API_WORKOUT_SHEET = os.environ.get("API_WORKOUT_SHEET")
APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
APP_AUTH = os.environ.get("APP_AUTH")

header_exercise = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

header_sheet = {
    "Authorization": APP_AUTH
}

# ---------------------------------- TIME AND DATE ----------------------------------
date = dt.datetime.now()
date_format = date.strftime("%d/%m/%Y")
time_format = date.strftime("%H:%M:%S")


def add_exercise():
    """Takes users input (workouts and duration) in a sentence and post the input to the exercise api. Retrieves the
    calculation for burned calories etc. These results get formatted and then will be posted to the datasheet. """
    exercise = input("What exercises did you do? ")

    p_exercise = {
        "query": exercise,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }

    exercise_response = requests.post(url=API_EXERCISE, json=p_exercise, headers=header_exercise)
    exercise_response.raise_for_status()

    data = exercise_response.json()
    list_exercises = data["exercises"]
    p_workout = {"workout": ""}

    for i in list_exercises:
        p_workout["workout"] = {
            "date": date_format,
            "time": time_format,
            "exercise": i["name"].title(),
            "duration": i["duration_min"],
            "calories": i["nf_calories"]
        }

        spreadsheet_response = requests.post(url=API_WORKOUT_SHEET, json=p_workout, headers=header_sheet)
        spreadsheet_response.raise_for_status()


add_exercise()

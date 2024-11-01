from fastapi import FastAPI

from package_folder.models.model import pred
from package_folder.models.data_load_and_process import load_and_preprocess
from package_folder.models.main import possible_matches


# Creating a FastAPI instance

app = FastAPI()

# To create a FastAPI endpoint we can use the "@" simple and pass the access to
# the endpoint for people to access it

@app.get("/")
def root():
    return {'greetings':'🚀 Welcome to the booklore api ! 🚀'}

@app.get("/dumb_model")
def prediction(sepal_length, sepal_width, petal_length, petal_width):
    prediction = pred(sepal_length, sepal_width, petal_length, petal_width)
    return {"prediction": int(prediction[0])}

@app.get('/recommendations')
def get_possible_matches(input_title: str):
    data = possible_matches(input_title)

    if isinstance(data, dict) and "error" in data:
        return data  # Renvoyer l'erreur

    return {"possible matches": data}

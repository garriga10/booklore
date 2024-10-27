from fastapi import FastAPI

from package_folder.models.model import pred

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

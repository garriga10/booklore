from fastapi import FastAPI
import pdb

from package_folder.workflow.model_reco_1 import pred
from package_folder.workflow.data_load_and_process import load_and_preprocess
from package_folder.workflow.main import possible_matches
from package_folder.workflow.DL_model import pred_DL
from package_folder.workflow.library_book_info import library_book_info

# Creating a FastAPI instance

app = FastAPI()

# To create a FastAPI endpoint we can use the "@" simple and pass the access to
# the endpoint for people to access it

@app.get("/")
def root():
    return {'greetings':'🚀 Welcome to the booklore api ! 🚀'}

@app.get('/recommendations')
def get_possible_matches(input_title: str):
    data = possible_matches(input_title)

    if isinstance(data, dict) and "error" in data:
        return data  # Renvoyer l'erreur

    return {"possible matches": data}

@app.get('/model-suggest')
def get_model_recommendations(bookid:str):
    reco = pred(bookid)
    return {'suggestions':reco}

@app.get('/DL_model-suggest')
def get_DL_model_recommendations(bookid:str):
    reco = pred_DL(bookid)
    return {'suggestions':reco}

@app.get('/book-info')
def get_book_info(bookid:str):
    book_info = library_book_info(bookid)
    return {'book-info':book_info}

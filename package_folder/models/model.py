import os
import pickle

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

def pred(sepal_length, sepal_width, petal_length, petal_width):
    model_path = os.path.join(ROOT_PATH,'models','model.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    # Use the model to predict the given inputs
    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])

    return prediction

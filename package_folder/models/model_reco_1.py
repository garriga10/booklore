import os
import pickle
from package_folder.models.model_settings import model_settings
from package_folder.models.data_load_and_process import load_and_preprocess

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

filtered_df = load_and_preprocess()[0]
book_features = load_and_preprocess()[1]


def pred(bookid: str, top_n=5):
    model_path = os.path.join(ROOT_PATH, 'models', 'model-reco-1.pkl')

    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    # Extraire le numéro de l'identifiant du livre
    book_index = int(bookid.split('.')[0])

    # Utiliser la ligne de DataFrame pour conserver les noms de colonnes
    distances, indices = model.kneighbors(book_features.iloc[[book_index]], n_neighbors=top_n + 1)

    recommended_books = filtered_df.iloc[indices[0][1:]]
    recommended_books = recommended_books[['title', 'author', 'publisher', 'rating']].copy()
    recommended_books['distance'] = distances[0][1:]
    recommended_books = recommended_books[['title', 'author', 'publisher', 'rating', 'distance']].to_dict(orient='records')
    #adding the Not Found string
    return recommended_books

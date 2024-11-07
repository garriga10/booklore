import os
import pickle
from package_folder.workflow.data_load_and_process import load_and_preprocess

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

filtered_df,book_features = load_and_preprocess()


def pred(bookid: str, top_n=5):
    model_path = os.path.join(ROOT_PATH, 'workflow','models', 'model-reco-1.pkl')

    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    # Extraire le numéro de l'identifiant du livre
    book_index = int(bookid.split('.')[0])

    # Identifying the nearest neighbors of the bookid
    distances, indices = model.kneighbors(book_features.iloc[[book_index]], n_neighbors=top_n + 1)

    recommended_books = filtered_df.iloc[indices[0][1:]] #filtering the original df with the nearest books we identified
    recommended_books = recommended_books[['title', 'genres','author','publisher','description','rating','coverImg']].copy()
    recommended_books['distance'] = distances[0][1:]
    recommended_books = recommended_books.fillna("Not available")
    recommended_books = recommended_books[['title', 'genres','author','publisher','description','rating','coverImg']].to_dict(orient='records')
    return recommended_books

import os
import pickle
import re
from package_folder.workflow.data_load_and_process import load_and_preprocess
from package_folder.workflow.load_pipe import preprocessor_pipe

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

filtered_df,book_features = preprocessor_pipe()


def pred(bookid: str, top_n=5):
    model_path = os.path.join(ROOT_PATH, 'workflow','models', 'model-reco-3.pkl')

    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    print(f'✅ Model loaded ✅')

    # Extraire le numéro de l'identifiant du livre
    book_index = int(re.match(r'^\d+', bookid).group())

    # Identifying the nearest neighbors of the bookid
    book_features_row = book_features[book_features['bookId']== str(book_index)].drop(columns=['bookId'])
    distances, indices = model.kneighbors(book_features_row,n_neighbors=top_n + 1)

    print(f'✅ Prediction valid ✅')

    recommended_books = filtered_df.iloc[indices[0][1:]] #filtering the original df with the nearest books we identified
    recommended_books = recommended_books[['title', 'genres','author','publisher','description','rating','coverImg']].copy()
    recommended_books['distance'] = distances[0][1:]
    recommended_books = recommended_books.fillna("Not available")
    recommended_books = recommended_books[['title', 'genres','author','publisher','description','rating','coverImg']].to_dict(orient='records')
    return recommended_books

pred('5881.Harry_Potter_and_the_Chamber_of_Secrets')

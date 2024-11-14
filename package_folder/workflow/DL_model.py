import os
import pickle
import re
import numpy as np
from package_folder.workflow.data_load_and_process import load_and_preprocess_DL

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

book_features = load_and_preprocess_DL()


def pred_DL(bookid: str, top_n=5):

    model_path = os.path.join(ROOT_PATH, 'workflow','models', 'DL_model.pkl')
    with open(model_path, 'rb') as file:
        knn = pickle.load(file)

    print(f'✅ Model loaded ✅')

    book_index = int(re.match(r'^\d+', bookid).group())

    # Identifying the nearest neighbors of the bookid
    embeddings_matrix = np.vstack(book_features['embed'].values)
    target_embedding = embeddings_matrix[book_features[book_features['bookId']==str(book_index)].index[0]]
    target_embedding = target_embedding.reshape(1,-1)

    distance,indices = knn.kneighbors(target_embedding,n_neighbors=top_n+1)
    similar_books_indices = indices[0][1:]
    similar_books = book_features.iloc[similar_books_indices][['title', 'genres','author','publisher','description','rating','coverImg']].fillna('not available')
    similar_books = similar_books.fillna("Not available")
    similar_books = similar_books.to_dict(orient='records')
    print(f'✅ Prediction valid ✅')

    return similar_books

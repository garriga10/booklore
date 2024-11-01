import pandas as pd
import ast
import os

from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))

def load_and_preprocess():

    # Load and preprocess the dataset
    file_path = os.path.join(project_root,'raw_data','goodreads.csv')
    goodreads_df = pd.read_csv(file_path)
    goodreads_df = goodreads_df.dropna(subset=['genres', 'rating', 'numRatings'])
    goodreads_df['genres'] = goodreads_df['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    filtered_df = goodreads_df[(goodreads_df['numRatings'] >= 1000) & (goodreads_df['rating'] >= 3.5)]

    # Encode the genres and scale ratings
    mlb = MultiLabelBinarizer()
    genre_features = mlb.fit_transform(filtered_df['genres'])
    scaler = MinMaxScaler()
    rating_features = scaler.fit_transform(filtered_df[['rating']])

    # Combine genre and rating features
    book_features = pd.concat([
    pd.DataFrame(genre_features, columns=mlb.classes_),
    pd.DataFrame(rating_features, columns=['scaled_rating'])
    ], axis=1)

    return filtered_df, book_features

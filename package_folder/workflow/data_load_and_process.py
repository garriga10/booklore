import pandas as pd
import ast
import os
import pdb
import re

from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))

def load_and_preprocess():

    # Load and preprocess the dataset
    file_path = os.path.join(project_root,'raw_data','goodreads.csv')
    goodreads_df = pd.read_csv(file_path)

    # Drop rows with missing essential data and parse genres
    goodreads_df = goodreads_df.dropna(subset=['genres', 'rating', 'numRatings'])
    goodreads_df['genres'] = goodreads_df['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

    # Setting up a pre filtered_df and defining the book_id for each entry
    filtered_df = goodreads_df[(goodreads_df['numRatings'] >= 1000) & (goodreads_df['rating'] >= 3.5)].reset_index(drop=True)
    filtered_df['bookId'] = filtered_df['bookId'].apply(lambda x: str(re.match(r'^\d+', x).group()) if isinstance(x, str) else None)

    # Ohe
    mlb = MultiLabelBinarizer()
    genre_features = mlb.fit_transform(filtered_df['genres'])
    genre_features_df = pd.DataFrame(genre_features, columns=mlb.classes_).reset_index(drop=True)

    # MinMax Scaler
    scaler = MinMaxScaler()
    rating_features = scaler.fit_transform(filtered_df[['rating']])
    rating_features_df = pd.DataFrame(rating_features, columns=['scaled_rating']).reset_index(drop=True)

    # Combining them alltogether
    book_features = pd.concat([
        filtered_df[['bookId']].reset_index(drop=True),
        genre_features_df,
        rating_features_df
    ],
                            axis=1)

    return filtered_df, book_features

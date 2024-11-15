import pandas as pd
import ast
import os
import re
from pathlib import Path

# Pipelining

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline,FunctionTransformer
from sklearn.impute import SimpleImputer

from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder,MinMaxScaler


def preprocessor_pipe():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))
    file_path = os.path.join(project_root,'raw_data','goodreads.csv')
    goodreads_df = pd.read_csv(file_path)
    goodreads_df['genres'] = goodreads_df['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    goodreads_df['bookId'] = goodreads_df['bookId'].apply(lambda x: str(re.match(r'^\d+', x).group()) if isinstance(x, str) else None)

    features_df = goodreads_df[['bookId','genres','publisher','edition','numRatings','rating']]

    # Categorical transformer

    ohe = OneHotEncoder(sparse_output=False)
    simple = SimpleImputer(strategy='most_frequent')

    c_ohe_pipe = Pipeline([
        ('Most frequent filler',simple),
        ('Encoder',ohe)
    ])

    c_mlb_pipe = Pipeline([
        ('multi_label', FunctionTransformer(lambda x: MultiLabelBinarizer().fit_transform(x), validate=False))
    ])

    categ_transfo = ColumnTransformer([
        ('One hot pipe',c_ohe_pipe,['publisher','edition']),
        ('Multi label pipe',c_mlb_pipe,'genres')
    ])

    # Numerical transformer

    num_transfo = Pipeline([
        ('Simple_imputer',SimpleImputer(strategy='mean')),
        ('Scale',MinMaxScaler())
    ])

    preprocessor = ColumnTransformer([
        ('categorical',categ_transfo,['genres','publisher','edition']),
        ('numerical',num_transfo,['numRatings','rating'])
    ],
        remainder='passthrough' #Passthrough: It keeps untransformed columns as they are in the output.
    )

    # Putting it alltogether and renaming the bookId column

    book_features = pd.DataFrame(preprocessor.fit_transform(features_df)).reset_index(drop=True)
    book_features.rename(columns={book_features.columns[-1]:'bookId'},inplace=True)
    return goodreads_df,book_features

import os
import pickle
import re
import pandas as pd
import numpy as np
from package_folder.workflow.data_load_and_process import load_and_preprocess_DL

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))

def library_book_info(library_bookid):
    file_path = os.path.join(project_root,'raw_data','goodreads.csv')
    goodreads_df = pd.read_csv(file_path)
    goodreads_df['bookId'] = goodreads_df['bookId'].apply(lambda x: str(re.match(r'^\d+', x).group()) if isinstance(x, str) else None)

    library_bookid = int(re.match(r'^\d+', library_bookid).group())

    library_info_row = goodreads_df[goodreads_df['bookId']== str(library_bookid)].drop(columns=['bookId'])
    book_info = library_info_row[['title', 'genres','author','publisher','description','rating','coverImg']].to_dict(orient='records')
    return book_info

from package_folder.models.data_load_and_process import load_and_preprocess
from package_folder.models.model_settings import model_settings

# 1. Loading and processing data

filtered_df = load_and_preprocess()[0]
book_features = load_and_preprocess()[1]

# 2. fitting the model on the book_features

model = model_settings(book_features)

def possible_matches(input_title, df=filtered_df):

    matches = df[df['title'].str.contains(input_title, case=False, na=False)]

    if matches.empty:
        return f"No books found with title containing '{input_title}'."

    # If multiple matches are found, prompt the user to select one
    if len(matches) > 1:
        possible_list = {i + 1: title for i, title in enumerate(matches['title'])}
        return possible_list

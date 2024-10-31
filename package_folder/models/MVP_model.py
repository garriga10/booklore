import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import ast

# Load and preprocess the dataset
goodreads_df = pd.read_csv('raw_data/goodreads.csv')
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

# Fit the KNN model
knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
knn_model.fit(book_features)

def knn_recommendations(input_title, df, knn_model, top_n=5):
    """
    Get top  book recommendations using a KNN model, allowing partial title input.

    Parameters:
    - input_title (str): Partial or full title of the book for recommendations.
    - df (pd.DataFrame): DataFrame containing book information and features.
    - knn_model (NearestNeighbors): Fitted KNN model.
    - top_n (int): Number of recommendations to return (default is 5).

    Returns:
    - recommendations (pd.Series or str): Series with recommended book titles, or a message if not found.
    """
    # Search for books with titles containing the input title
    matches = df[df['title'].str.contains(input_title, case=False, na=False)]

    if matches.empty:
        return f"No books found with title containing '{input_title}'."

    # If multiple matches are found, prompt the user to select one
    if len(matches) > 1:
        print("Multiple matches found. Please select the number corresponding to your book:")
        for idx, title in enumerate(matches['title'], 1):
            print(f"{idx}. {title}")

        # Get the user's selection
        while True:
            try:
                selection = int(input("Enter the number of your selected book: "))
                if 1 <= selection <= len(matches):
                    selected_title = matches.iloc[selection - 1]['title']
                    break
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        selected_title = matches.iloc[0]['title']
        print(f"Found match: '{selected_title}' for input '{input_title}'")

    # Find the index of the selected book
    book_idx = df[df['title'] == selected_title].index[0]

    # Find distances and indices of the nearest neighbors
    distances, indices = knn_model.kneighbors([book_features.iloc[book_idx]], n_neighbors=top_n+1)

    # Extract information for recommended books
    recommended_books = df.iloc[indices[0][1:]]
    recommended_books = recommended_books[['title', 'author', 'publisher', 'rating']].copy()
    recommended_books['distance'] = distances[0][1:]

    return recommended_books

if __name__ == "__main__":
    # Interactive input for the user
    user_input_title = input("Enter a book title or partial title: ")
    recommendations = knn_recommendations(user_input_title, filtered_df, knn_model)

    # Display recommendations
    print("Recommended books:")
    print(recommendations)

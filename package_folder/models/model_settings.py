from sklearn.neighbors import NearestNeighbors

# Fit the KNN model
def model_settings(book_features):
    knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
    knn_model.fit(book_features)
    return knn_model

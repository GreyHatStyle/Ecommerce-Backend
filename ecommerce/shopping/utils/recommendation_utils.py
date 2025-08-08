import os

import joblib
from django.conf import settings
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ..models import Product

# Loading it as soon as the django starts running
model_imp = joblib.load(
    os.path.join(settings.BASE_DIR, "shopping", "ml_model", "recommend_cluster.pkl")
)
vec = joblib.load(
    os.path.join(settings.BASE_DIR, "shopping", "ml_model", "recom_vectorizer.pkl")
)


class ProductRecommendationUtil:
    
    def __init__(self):
        
        self.df: DataFrame
        
        self.model: KMeans = model_imp
        self.vectorizer: TfidfVectorizer = vec
        
        self.X = None
        self.cluster_labels = None
        
        self.__load_all_products()
        
        
    def __load_all_products(self):
        """
        Takes all products from "product table" and sets it to `self.db` dataframe for further processing.
        """
        
        product = Product.objects.all().values('id', 'description', 'recommendation_cluster')
        
        # TODO: For now loading all data in Dataframe, find a scalable approach which don't takes whole db into server's RAM.
        self.df = DataFrame(product)
        
        
    def predict_cluster_number(self, description: str) -> int:
        """
        Predicts the cluster for new products description
        
        Args:
            description (str): New product's description

        Returns:
            int: cluster number
        """
        description_vector = self.vectorizer.transform([description])
        cluster = self.model.predict(description_vector)[0]
        return cluster

    
    def search_products(self, query: str, top_n=10) -> list:
        """
        Basically takes the query string, vectorize it, find cluster, and finds the best correlated(cosine) description indexes.

        Args:
            query (str): Give user search query here (like: solar panel, cloths)
            top_n (int, optional): How many top `top_n` results do you want.

        Returns:
            list: list of all `product uuid`'s which can be used to filter and display on search.
        """
        
        self.X = self.vectorizer.transform(self.df['description'])
        
        query_vector = self.vectorizer.transform([query])
        
        predicted_cluster = self.model.predict(query_vector)[0]
        
        # print("Predicted Cluster: ", predicted_cluster)
        # print(self.df.head(4))
        
        cluster_products:DataFrame = self.df[self.df['recommendation_cluster'] == predicted_cluster]
        
        if len(cluster_products) == 0:
            return self._fallback_search(query, top_n)
        
        cluster_indices = cluster_products.index
        cluster_vectors = self.X[cluster_indices]
        
        similarities = cosine_similarity(query_vector, cluster_vectors).flatten()
        

        top_indices = similarities.argsort()[-top_n:][::-1]
        recommended_products = cluster_products.iloc[top_indices]
        
        product_id_list: list = recommended_products['id'].to_list()
        return product_id_list
    
    def _fallback_search(self, query, top_n) -> list[str]:
        """
        Fallback to similarity search across all products
        """
        similarities = cosine_similarity(
            self.vectorizer.transform([query]), 
            self.X
        ).flatten()
        
        top_indices = similarities.argsort()[-top_n:][::-1]
        product_id_list: list = self.df.iloc[top_indices]['id'].to_list()
        
        return product_id_list 
    
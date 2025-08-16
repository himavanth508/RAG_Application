from pymongo import MongoClient
import os

MONGO_URI = "mongodb+srv://himavanth508:12345@cluster0.643ybf9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with actual URI
client = MongoClient(MONGO_URI)

db = client["my_rag_app"]  # You can name the DB anything
users_collection = db["users"]
vectors_collection = db["vector_embeddings"]
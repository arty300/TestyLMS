from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.MONGO_URI)
db = client.get_default_database()
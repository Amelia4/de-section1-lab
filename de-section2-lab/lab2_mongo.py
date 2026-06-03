from pymongo import MongoClient

# Ganti dengan URI Atlas jika menggunakan Atlas
client = MongoClient(
    "mongodb://localhost:27017/"
)

db = client["store_db"]

print("Berhasil terhubung ke MongoDB!")
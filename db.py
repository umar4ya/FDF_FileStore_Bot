# from pymongo import MongoClient
# import os

# def get_db():
#     client = MongoClient(os.getenv('MONGO_URI'))
#     db = client['telegram_bot']
#     db_collection = db['files']
#     return db

# def save_file(file_id, file_name, file_keywords):
#     db = get_db()
#     db.files.insert_one({
#         "file_id": file_id,
#         "file_name": file_name,
#         "file_keywords": file_keywords
#     })

# # def search_files(query):
# #     db = get_db()
# #     return db.files.find({"file_keywords": {"$regex": query, "$options": "i"}})

# def search_files(file_id):
#     return db_collection.find({'file_id': file_id})


from pymongo import MongoClient
import os

def get_db():
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client['telegram_bot']
    db_collection = db['files']
    return db, db_collection  # Return both db and db_collection

def save_file(file_id, file_name, file_keywords):
    db, db_collection = get_db()  # Retrieve db and db_collection
    db_collection.insert_one({
        "file_id": file_id,
        "file_name": file_name,
        "file_keywords": file_keywords
    })

def search_files(query):
    db, db_collection = get_db()  # Retrieve db and db_collection
    return db_collection.find({"file_keywords": {"$regex": query, "$options": "i"}})


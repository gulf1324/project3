from pymongo import MongoClient
import pandas as pd
import csv

HOST = 'cluster0.fck42qv.mongodb.net'
USER = 'project3'
PASSWORD = '1324'
DATABASE_NAME = 'fifa_cleaned'
COLLECTION_NAME = 'fifa_cleaned'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient({MONGO_URI})

data = pd.read_csv('fifa_cleaned.csv', index_col= 0)
header = data.columns

with open('fifa_cleaned.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        rows = {}
        for field in header:
            rows[field]= row[field]
            
        collection = client[DATABASE_NAME][COLLECTION_NAME]
        collection.insert_one(rows)
import sqlite3
from xgboost import XGBRegressor
from category_encoders import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
import pickle

def DB_to_X_y():
    conn = sqlite3.connect("player_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.age, b.height_cm, b.weight_kgs, b.body_type, b.balance, v.overall_rating, v.tags, s.skill_moves, v.value_euro 
        FROM player_biology b 
        LEFT JOIN player_stats s ON b.id = s.id
        LEFT JOIN player_value v ON s.id = v.id """) # 8개 feature(이후 feature importance 계산하여 조절)

    data = cursor.fetchall()
    X = [row[:-1] for row in data]
    y = [row[-1] for row in data]
    
    for i in range(len(y)):
        if y[i] == '':
            y[i] = sum(filter(lambda i: isinstance(i, int), y))/len(y)   # y unique 값 -> int, str(''), int만 sum
    return X, y

def model_fit(X, y):
    
    preprocess_pipeline = make_pipeline(OrdinalEncoder(), SimpleImputer()) 
    model = XGBRegressor()

    X_preprocessed = preprocess_pipeline.fit_transform(X)
    
    model.fit(X_preprocessed,y)        # y결측값 -> 평균으로

    return model




X, y = DB_to_X_y()
model = model_fit(X, y)

with open('model.pkl','wb') as pickle_file:
        pickle.dump(model, pickle_file)




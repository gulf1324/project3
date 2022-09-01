import sqlite3
from pymongo import MongoClient
import os

HOST = 'cluster0.fck42qv.mongodb.net'
USER = 'project3'
PASSWORD = '1324'
DATABASE_NAME = 'fifa_cleaned'
COLLECTION_NAME = 'fifa_cleaned'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

DB_FILENAME = 'player_data.db'
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)

client = MongoClient(MONGO_URI)
collection =client[DATABASE_NAME][COLLECTION_NAME]

def create_sqlite_table():                     # rdb 테이블 생성
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS player_biology")  # 선수들 능력치 크게 세 분야로 분류
    cursor.execute("DROP TABLE IF EXISTS player_value")
    cursor.execute("DROP TABLE IF EXISTS player_stats")

    cursor.execute("""CREATE TABLE player_biology (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        age INTEGER,
                        height_cm NUMERIC,
                        weight_kgs NUMERIC,
                        body_type VARCHAR(100),
                        balance INTEGER
                        );""")

    cursor.execute("""CREATE TABLE player_value (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        
                        overall_rating INTEGER,
                        value_euro NUMERIC,
                        wage_euro NUMERIC,
                        international_reputation INTEGER,
                        release_clause_euro NUMERIC,
                        club_rating INTEGER,
                        tags INTEGER,
                        FOREIGN KEY (id) REFERENCES player_biology(id)
                        );
                         """)

    cursor.execute("""CREATE TABLE player_stats (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            
                            skill_moves INTEGER,
                            national_team INTEGER,
                            finishing INTEGER,
                            volleys INTEGER,
                            dribbling INTEGER,
                            acceleration INTEGER,
                            agility INTEGER,
                            FOREIGN KEY (id) REFERENCES player_biology(id)
                            );
                            """)
    cursor.close()                    
    conn.close()

def move_to_rdb(collection):                   # nosql에서 rdb로 
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    for item in collection.find():

        cursor.execute("""INSERT INTO player_biology (age, height_cm, weight_kgs, body_type, balance) VALUES (?,?,?,?,?)""", 
            (
            item['age'],
            item['height_cm'],
            item['weight_kgs'],
            item['body_type'],
            item['balance']
            ))

        cursor.execute("""INSERT INTO player_value (overall_rating, value_euro, wage_euro, international_reputation, release_clause_euro, club_rating, tags) VALUES (?,?,?,?,?,?,?)""", 
            (
            item['overall_rating'],
            item['value_euro'],
            item['wage_euro'],
            item['international_reputation(1-5)'],
            item['release_clause_euro'],
            item['club_rating'],
            item['tags']
            ))
        
        cursor.execute("""INSERT INTO player_stats (skill_moves, national_team, finishing, volleys, dribbling, acceleration, agility) VALUES (?,?,?,?,?,?,?)""", 
            (
            item['skill_moves(1-5)'],
            item['national_team'],
            item['finishing'],
            item['volleys'],
            item['dribbling'],
            item['acceleration'],
            item['agility']
            ))
        
        conn.commit()
    cursor.close()
    conn.close()
        
create_sqlite_table()
move_to_rdb(collection)
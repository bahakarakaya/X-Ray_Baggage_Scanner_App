import psycopg2
from psycopg2.extras import RealDictCursor  # To return sql queries as dict (like row["label"])
import os
from dotenv import load_dotenv

# imports db information that is inside .env
load_dotenv()

# db info to be connected
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Function to connect to database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor  # returns JSON-like dict
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        raise

def insert_prediction(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO predictions (image_id, objects_detected, status)
            VALUES (%s, %s, %s)
        """, (
            data["image_id"],
            data["objects_detected"],
            data["status"]
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()     #reverts all changes to prevent corrupting db
        print("Error while inserting:", e)
        raise
    finally:
        cursor.close()
        conn.close()

def get_predictions():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM predictions ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print("Error while fetching predictions:", e)
        return []
    finally:
        cursor.close()
        conn.close()

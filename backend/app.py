from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='static')
CORS(app)
load_dotenv()

# Get database credentials from environment variables

def connect_to_db():
    try:
        conn = psycopg2.connect(
            
             dbname='myappdb',
            user='myuser',
            password='mypassword',
            host='35.193.6.168',
            port='5432',
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
        return None

@app.route('/', methods=['POST'])
def upload_to_database():
    name = request.form.get('name')
    city = request.form.get('country')

    conn = connect_to_db()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO mytable (name, country) VALUES (%s, %s)", (name, country))
        conn.commit()
        return jsonify({'message': 'Data uploaded successfully'}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Failed to upload data to database.Please eneter the correct details', 'details': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


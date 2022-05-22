import os
from flask import Flask
# from flask_cors import CORS
# from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# CORS(app)
# mysql = MySQL(app)

# app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
# app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
# app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
# app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)

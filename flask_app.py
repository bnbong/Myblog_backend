import os
import sqlite3
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for
# from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row()
    return conn

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)

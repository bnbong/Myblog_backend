import os
import sqlite3
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for
# from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    db_notes = conn.execute('SELECT id, created, content FROM notes;').fetchall()
    conn.close()

    notes = []
    for note in db_notes:
        note = dict(note)
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)

    # return (f"{note['id'], note['created']}")
    return notes

if __name__ == '__main__':
    app.run(debug=True)

import os
import sqlite3
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for
# from flask_cors import CORS
from dotenv import load_dotenv

template_dir = os.path.abspath('../Myblog_frontend/templates')

load_dotenv()

app = Flask(__name__, template_folder=template_dir)
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

    # index.html from Myblog_frontend
    return render_template('index.html', notes=notes)

if __name__ == '__main__':
    app.run(debug=True)

import os
import sys
import sqlite3
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for
# from flask_cors import CORS
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Myblog_frontend.flask_render_page import *

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

    # index.html from Myblog_frontend
    # return render_template('index.html', notes=notes)
    render_mainpage(notes)

if __name__ == '__main__':
    app.run(debug=True)

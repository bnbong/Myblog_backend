import os
import sqlite3
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for
# from flask_cors import CORS
from dotenv import load_dotenv

template_dir = os.path.abspath('../Myblog_frontend/templates_2')

load_dotenv()

app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    db_notes = conn.execute('SELECT id, title, created, content FROM notes;').fetchall()
    conn.close()

    notes = []
    for note in db_notes:
        note = dict(note)
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)

    # index.html from Myblog_frontend
    # return render_template('index.html', notes=notes)
    return render_template('index.html')

@app.route('/create/', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
            return redirect(url_for('index'))

        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))

        conn.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('create.html')

# @app.route('/<int:id>/edit', methods=('GET', 'POST'))
# def edit(id):
#     pass

# @app.route('/<int:id>/delete/', methods=('POST',))
# def delete(id):
#     pass

if __name__ == '__main__':
    app.run(debug=True)

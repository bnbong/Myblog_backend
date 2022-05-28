from app import app
from app import db
from app.models import Post

import os
import sqlite3
import markdown

from flask import render_template, request, flash, redirect, url_for

# db connection function for test
def get_db_connection():
    database_dir = os.path.abspath('../Myblog_backend/Database/app.db')

    conn = sqlite3.connect(database_dir)
    conn.row_factory = sqlite3.Row
    return conn

# fetching databases for test
def get_notes():
    conn = get_db_connection()
    db_notes = conn.execute('SELECT id, title, created, content FROM notes;').fetchall()
    conn.close()

    notes = []
    for note in db_notes:
        note = dict(note)
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)
    return notes

def get_posts():
    posts = Post.query.order_by(Post.created.desc()).all()
    return posts

@app.route('/')
def index():
    # page = request.args.get('page',type=int,default=1)
    # notes = get_notes()
    posts = get_posts()
    # notes = notes.paginate(page, per_page=5)
    
    # # for setting newest post to the front.
    # notes = notes.reverse()

    # index.html from Myblog_frontend
    # return render_template('index.html', notes=notes)
    return render_template('index.html', notes=posts)

@app.route('/aboutme')
def aboutme():
    about_me = Post.query.filter_by(title='About Me').first()

    return render_template('postview.html', note=about_me)

@app.route('/posts/<post_id>')
def postview(post_id):
    posts = get_posts()
    post_id = int(post_id) - 1
    selected_post = posts[post_id]

    return render_template('postview.html', note=selected_post)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    # conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        content = markdown.markdown(content)

        if not title:
            flash('Title is required!')
            return redirect(url_for('index'))

        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        # conn.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content,))
        # conn.commit()
        # conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# @app.route('/<int:id>/edit', methods=('GET', 'POST'))
# def edit(id):
#     pass

# @app.route('/<int:id>/delete/', methods=('POST',))
# def delete(id):
#     pass
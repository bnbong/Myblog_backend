from app import app
from app import db
from app.models import Post

import os
import sqlite3
import markdown

from flask import render_template, request, flash, redirect, url_for

ROWS_PER_PAGE = 5

def get_posts():
    posts = Post.query.order_by(Post.created.desc()).all()

    return posts

@app.route('/')
def index():
    page = request.args.get('page', type=int, default=1)
    posts = Post.query.order_by(Post.created.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('index.html', posts=posts)

@app.route('/<category>')
def category_view(category):
    page = request.args.get('page', type=int, default=1)
    category_posts = Post.query.filter_by(tag=category).paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('index.html', posts=category_posts)

@app.route('/aboutme')
def aboutme():
    about_me = Post.query.filter_by(title='About Me').first()

    return render_template('postview.html', post=about_me)

@app.route('/posts/<post_id>')
def postview(post_id):
    # posts = get_posts()
    post_id = int(post_id)
    selected_post = Post.query.filter_by(id=post_id).first()

    return render_template('postview.html', post=selected_post)

# @app.route('/create/', methods=('GET', 'POST'))
# def create():

#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         content = markdown.markdown(content)

#         if not title:
#             flash('Title is required!')
#             return redirect(url_for('index'))

#         if not content:
#             flash('Content is required!')
#             return redirect(url_for('index'))

#         new_post = Post(title=title, content=content)
#         db.session.add(new_post)
#         db.session.commit()

#         return redirect(url_for('index'))

#     return render_template('create.html')

# @app.route('/<int:id>/edit', methods=('GET', 'POST'))
# def edit(id):
#     pass

# @app.route('/<int:id>/delete/', methods=('POST',))
# def delete(id):
#     pass
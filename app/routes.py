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
    category_posts = Post.query.filter_by(tag=category)
    category_posts = category_posts.order_by(Post.created.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('index.html', posts=category_posts)

@app.route('/aboutme')
def aboutme():
    about_me = Post.query.filter_by(title='About Me').first()

    return render_template('postview.html', post=about_me)

@app.route('/posts/<post_id>')
def postview(post_id):
    post_id = int(post_id)
    selected_post = Post.query.filter_by(id=post_id).first()

    return render_template('postview.html', post=selected_post)

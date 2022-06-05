# TODO: make fuctions which update existing posts when they updated. 

from app.models import Post
from app import db
from datetime import datetime

import os
import markdown

delete_all_posts_from_DB()

post_dir = os.path.abspath('../Myblog_posts/posts')
category_name_lists = os.listdir(post_dir)

# possible category lists:
# IT, Study, Hobby, My_Daily_Life, Development, Game = \
#     listdirname[0], listdirname[1], listdirname[2], listdirname[3], listdirname[4], listdirname[5]

for category in category_name_lists:
  post_dates = os.listdir(os.path.join(post_dir, category))

  db_selected = Post.query.filter_by(tag=category).all()
  db_dates = []
  for post in db_selected:
      db_dates.append(post.get_exact_created())

  for date in post_dates:
      year, month, day, hour, minute, sec = split_datestring_into_datetime(date)
      new_date = datetime(year, month, day, hour, minute, sec)

      # checking and add newest posts at selected categories
      if str(new_date) not in db_dates:
          post_created = new_date
          post_title = get_title_from_txt_file()
          post_thumbnail_url = get_thumbnail_url_from_txt_file()
          post_content = get_markdowned_content_from_txt_file()

          new_post = Post(title=post_title, thumbnail_url=post_thumbnail_url, content=post_content, \
              content_preview=post_content_preview, created=post_created, tag=category)

          db.session.add(new_post)

def delete_all_posts_from_DB():
    posts = Post.query.all()
    for post in posts:
        db.session.delete(post)

def split_datestring_into_datetime(date):
    year, month, day, hour, minute, sec = int(date[:4]), int(date[4:6]), int(date[6:8]),\
          int(date[8:10]), int(date[10:12]), int(date[12:14])

    return year, month, day, hour, minute, sec

def get_title_from_txt_file():
    with open(os.path.join(post_dir, category, date, 'title.txt'), 'r') as f1:
        post_title = f1.read()
        f1.close()
    
    return post_title

def get_thumbnail_url_from_txt_file():
    with open(os.path.join(post_dir, category, date, 'thumbnail.txt'), 'r') as f2:
        post_thumbnail_url = f2.read()
        f2.close()
    
    return post_thumbnail_url

def get_markdowned_content_from_txt_file():
    with open(os.path.join(post_dir, category, date, 'post.md'), 'r') as f3:
        post_content = f3.read()
        post_content_preview = post_content[:298] + ".."
        post_content_preview = markdown.markdown(post_content_preview)
        post_content = markdown.markdown(post_content)
        f3.close()

    return post_content

db.session.commit()

from app.models import Post
from app import db
from datetime import datetime

import os
import markdown


class GetPost:

    post_dir = os.path.abspath('../Myblog_posts/posts')
    category_name_lists = os.listdir(post_dir)
    category = None
    date = None


    def get_post_dir(self):
        return self.post_dir
    
    def get_category_name_lists(self):
        return self.category_name_lists

    def get_category(self):
        return self.category
    
    def get_date(self):
        return self.date


    def set_category(self, category):
        self.category = category
    
    def set_date(self, date):
        self.date = date

    def split_datestring_into_datetime(self, date):
        year, month, day, hour, minute, sec = int(date[:4]), int(date[4:6]), int(date[6:8]),\
            int(date[8:10]), int(date[10:12]), int(date[12:14])

        return year, month, day, hour, minute, sec

    def open_and_read_txt_file(self, file_name):
        with open(os.path.join(self.post_dir, self.category, self.date, file_name), 'r') as f:
            output = f.read()
            f.close()

            return output

    def get_title_from_txt_file(self):
        post_title = self.open_and_read_txt_file('title.txt')
        
        return post_title

    def get_thumbnail_url_from_txt_file(self):
        post_thumbnail_url = self.open_and_read_txt_file('thumbnail.txt')
        
        return post_thumbnail_url

    def get_markdowned_content_from_txt_file(self):
        post_content = self.open_and_read_txt_file('post.md') 
        post_content_preview = post_content[:298] + ".."
        post_content_preview = markdown.markdown(post_content_preview)
        post_content = markdown.markdown(post_content)

        return post_content, post_content_preview

    def get_post_data(self):
        post_created = self.get_date()
        post_title = self.get_title_from_txt_file()
        post_thumbnail_url = self.get_thumbnail_url_from_txt_file()
        post_content, post_content_preview = self.get_markdowned_content_from_txt_file()

        return post_created, post_title, post_thumbnail_url, post_content, post_content_preview


class GetNewPost(GetPost):

    def __init__(self, new_date):
        self.new_date = new_date


    def get_new_date(self):
        return self.new_date


    def set_new_date(self, new_date):
        self.new_date = new_date


    def get_new_post_data(self):
        post_created, post_title, post_thumbnail_url, post_content, post_content_preview \
            = super().get_post_data()

        post_created = self.get_new_date()

        return post_created, post_title, post_thumbnail_url, post_content, post_content_preview


class InitializeDB(GetNewPost):

    post_list = []

    def __init__(self):
        self.initialize_database()

    def get_post_list(self):
        return self.post_list

    def initialize_database(self):

        self.delete_all_posts_from_DB()

        # possible category lists:
        # IT, Study, Hobby, My_Daily_Life, Development, Game = \
        #     listdirname[0], listdirname[1], listdirname[2], listdirname[3], listdirname[4], listdirname[5]

        category_name_lists = self.get_category_name_lists()
        post_dir = self.get_post_dir()

        for category in category_name_lists:
            self.set_category(category)
            category = self.get_category()

            post_dates = os.listdir(os.path.join(post_dir, category))

            for date in post_dates:
                self.set_date(date)
                date = self.get_date()

                new_post_date = self.make_new_date_from_given_date(date)
                self.add_new_post_into_db(new_post_date)

        initialized_post_list = self.get_post_list()
        initialized_post_list.sort(key=lambda post: post.created, reverse=True)
        for post in initialized_post_list:
            db.session.add(post)
            
        db.session.commit()

    def delete_all_posts_from_DB(self):
        posts = Post.query.all()
        for post in posts:
            db.session.delete(post)

    def make_new_date_from_given_date(self, date):
        self.set_date(date)
        date = self.get_date()

        year, month, day, hour, minute, sec = self.split_datestring_into_datetime(date)
        new_date = datetime(year, month, day, hour, minute, sec)

        self.set_new_date(new_date)

        return self.get_new_date()

    def add_new_post_into_db(self, date):
        post_created, post_title,post_thumbnail_url, post_content, post_content_preview\
            = self.get_new_post_data()

        new_post = Post(title=post_title, thumbnail_url=post_thumbnail_url, content=post_content, \
            content_preview=post_content_preview, created=post_created, tag=self.get_category())

        self.post_list.append(new_post)


if __name__ == '__main__':
    InitializeDB()

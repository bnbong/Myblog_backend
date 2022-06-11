from app.models import Post
from app import db
from datetime import datetime

from init_db import InitializeDB

import os


class UpdatePost(InitializeDB):

    posts_at_db = []
    posts_at_folder = []
    
    def __init__(self):
        self.update_all_posts_data()


    def get_posts_at_db(self):
        return self.posts_at_db
    
    def get_posts_at_folder(self):
        return self.posts_at_folder
    

    def set_posts_at_db(self, posts_list):
        self.posts_at_db = posts_list
    
    def set_posts_at_folder(self, posts_list):
        self.posts_at_folder = posts_list


    def update_all_posts_data(self):
        '''
        cases of post updating:
            1. post updated (rename title or edited content)
            2. post deleted
            3. new post uploaded
        '''
        category_name_lists = self.get_category_name_lists()
        post_dir = self.get_post_dir()

        for category in category_name_lists:
            self.set_category(category)
            category = self.get_category()

            # get all posts' created date and amount of posts at db which Post.tag == category
            all_selected_category_db_posts = self.get_posts_list_at_selected_category_db(category).all()
            self.set_posts_at_db(all_selected_category_db_posts)

            # get all posts' created date and amount of posts at Myblog_posts folder which Post.tag == category
            all_selected_category_folder_posts = self.get_posts_list_at_selected_category_folder(category)
            self.set_posts_at_folder(all_selected_category_folder_posts)

            self.compare_db_and_folder_then_update_posts()

        db.session.commit()


    def get_posts_list_at_selected_category_db(self, category):
        posts = Post.query.filter_by(tag=category)

        return posts

    def get_posts_list_at_selected_category_folder(self, category):
        post_list = []

        all_dates_at_seleceted_category_folder = \
            os.listdir(os.path.join(self.post_dir, category))
        
        for date in all_dates_at_seleceted_category_folder:
            self.set_date(date)

            post_created, post_title, post_thumbnail_url, post_content, post_content_preview \
                = self.get_post_data()

            year, month, day, hour, minute, sec = self.split_datestring_into_datetime(date)
            post_created = datetime(year, month, day, hour, minute, sec)

            post = Post(title=post_title, thumbnail_url=post_thumbnail_url, content=post_content, \
            content_preview=post_content_preview, created=post_created, tag=category)

            post_list.append(post)

        return post_list

    def compare_db_and_folder_then_update_posts(self):
        size_of_selected_category_db = len(self.get_posts_at_db())
        size_of_selected_category_folder = len(self.get_posts_at_folder())

        # case 1. post updated (rename title or edited content)
        if size_of_selected_category_db == size_of_selected_category_folder:
            self.update_modified_posts()

        # case 2. post deleted
        elif size_of_selected_category_db > size_of_selected_category_folder:
            self.update_deleted_posts()

        # case 3. new post uploaded
        else:
            self.update_newly_uploaded_posts()

    def update_deleted_posts(self):
        # posts at db > posts at folder
        category = self.get_category()
        posts_at_folder = self.get_posts_at_folder()
        posts_at_db = self.get_posts_list_at_selected_category_db(category).all()

        # looks dirty...
        for post_1 in posts_at_folder:
            for post_2 in posts_at_db:
                if post_1.created == post_2.created:
                    posts_at_db.remove(post_2)

        deleted_posts = posts_at_db

        for post in deleted_posts:
            db.session.delete(post)

    def update_modified_posts(self):
        import markdown
        # modified posts is located at folder
        # created time cannot be modified.
        # need to upgrade -> comment will disappear!
        category = self.get_category()

        posts = self.get_posts_at_folder()

        for post in posts:
            date = post.created
            post_filtered_by_date = self.get_posts_list_at_selected_category_db(category).filter_by(created=date)
            post_filtered_by_date.update(dict(title=post.title, content=markdown.markdown(post.content), content_preview=post.content_preview))

    def update_newly_uploaded_posts(self):
        # posts at db < posts at folder
        category = self.get_category()
        posts_at_folder = self.get_posts_at_folder()
        posts_at_db = self.get_posts_list_at_selected_category_db(category).all()

        # looks dirty...
        for post_1 in posts_at_db:
            for post_2 in posts_at_folder:
                if post_1.created == post_2.created:
                    posts_at_folder.remove(post_2)

        added_posts = posts_at_folder

        for post in added_posts:
            db.session.add(post)


if __name__ == '__main__':
    UpdatePost()

import unittest
from app.routes import *


class Dotenv_Test(unittest.TestCase):
    
    def test_could_load_SECRET_KEY_from_env(self):
        from config import Config

        with open('.env', 'r') as f:
            _, secret_key_from_env = (f.read()).split('=')
            secret_key_from_env = secret_key_from_env[2:-1]

        self.assertEqual(secret_key_from_env, app.config['SECRET_KEY'])

class Markdown_Test(unittest.TestCase):

    def setUp(self):
        self.markdown_text = '## 👋 Hello world! - 한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )'
        self.long_md_text = '''
## 👋 Hello world!

 - 한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )
 - 대한민국 공군 ROKAF 병 825기 정보체계관리(30010 과정) (2021.04.12 ~ 2023.01.11)
 - GiftMusic backend 개발자 (2020.09 ~ 2021.04)
        '''
        self.block_text = ''' > this is block text'''
        self.hyperlink_text = ''' - [Follow Link Here](https://github.com/bnbong/bnbong.github.io)'''
        self.html_text_in_md = '''
## 💻 My Stacks
  
  - Language & Frameworks
<div>
<img src="https://img.shields.io/badge/Android%20Studio-FFFFFF?style=flat-square&logo=Android%20Studio"/>
</div>
        '''

    def test_could_convert_md_to_html(self):
        converted_text = markdown.markdown(self.markdown_text)
        
        self.assertEqual('<h2>👋 Hello world! - 한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )</h2>', converted_text)

    def test_could_convert_long_md_text(self):
        converted_text = markdown.markdown(self.long_md_text)

        self.assertEqual('''<h2>👋 Hello world!</h2>
<ul>
<li>한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )</li>
<li>대한민국 공군 ROKAF 병 825기 정보체계관리(30010 과정) (2021.04.12 ~ 2023.01.11)</li>
<li>GiftMusic backend 개발자 (2020.09 ~ 2021.04)</li>
</ul>''', converted_text)

    def test_could_convert_block_md_text(self):
        converted_text = markdown.markdown(self.block_text)
        
        self.assertEqual('''<blockquote>
<p>this is block text</p>
</blockquote>''', converted_text)

    def test_could_convert_hyperlink_md_text(self):
        converted_text = markdown.markdown(self.hyperlink_text)

        self.assertEqual('''<ul>
<li><a href="https://github.com/bnbong/bnbong.github.io">Follow Link Here</a></li>
</ul>''', converted_text)

    def test_is_double_markdown_function_work(self):
        # it working! double converting does not matter the text form.

        converted_text = markdown.markdown(self.markdown_text)

        self.assertEqual('<h2>👋 Hello world! - 한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )</h2>', converted_text)

        double_converted_text = markdown.markdown(converted_text)

        self.assertEqual('<h2>👋 Hello world! - 한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )</h2>', double_converted_text)
    
    def test_is_html_plus_md_text_could_be_converted(self):
        # it working! md text which contains html text not matter the converting function.
        converted_text = markdown.markdown(self.html_text_in_md)

        self.assertEqual('''<h2>💻 My Stacks</h2>
<ul>
<li>Language &amp; Frameworks</li>
</ul>
<div>
<img src="https://img.shields.io/badge/Android%20Studio-FFFFFF?style=flat-square&logo=Android%20Studio"/>
</div>''', converted_text)


class DB_Testcase_Root(unittest.TestCase):
    from app.models import Post
    from app import db

    from datetime import datetime

    import os
    import markdown

    def setUp(self):

        self.post_dir = os.path.abspath('../Myblog_posts/posts')
        self.category = 'Development'
        self.date = None
        self.category_dir = os.path.join(self.post_dir, self.category)
        

        test_created = self.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        test_date, test_time = test_created.split()
        Y, M, D = test_date.split('-')
        H, m, S = test_time.split(':')

        self.test_created_folder = Y+M+D+H+m+S

        test_folder = os.path.join(self.category_dir, self.test_created_folder)
        self.test_folder = test_folder

    def make_new_post(self):

        if not os.path.exists(self.test_folder):
            # make post folder
            os.mkdir(self.test_folder)

            test_title = 'This is Test title'
            test_url = 'https://thisistest.test/'
            test_category = self.category
            test_content = 'Hello world this is test content'
            test_content_preview = 'Hello world th..'

            self.make_file(os.path.join(self.test_folder, 'title.txt'), test_title)
            self.make_file(os.path.join(self.test_folder, 'thumbnail.txt'), test_url)
            self.make_file(os.path.join(self.test_folder, 'post.md'), test_content)

    def make_file(self, file_name, content):
        with open(file_name, 'w') as f:
            f.write(content)
            f.close()

class Database_Test(DB_Testcase_Root):

    def setUp(self):
        self.test_post = self.input_post_at_db()
        self.all_posts = Post.query.order_by(Post.created.desc()).all()

    def get_test_post(self):
        return self.test_post

    def get_all_posts(self):
        return self.all_posts

    def get_selected_post_by_title(self, title):
        return Post.query.filter_by(title=title)

    def set_all_posts(self, all_posts):
        self.all_posts = all_posts

    def set_test_post(self, post):
        self.test_post = post

    def input_post_at_db(self):
        test_title = 'Test title for testing'
        test_tag = 'IT'
        test_content = 'This is test content'
        test_content_preview = test_content[:300] + '..'
        test_created = self.datetime(2020,2,2,2,2,2)

        test_content = markdown.markdown(test_content)

        test_post = Post(title=test_title, tag=test_tag, content=test_content, \
            content_preview=test_content_preview, created=test_created)

        return test_post

    def insert_post_at_db(self, post):
        db.session.add(post)
        self.set_all_posts(Post.query.order_by(Post.created.desc()).all())

    # init db check
    def test_could_get_all_posts_is_at_db(self):
        self.assertEqual(4, len(self.get_all_posts()))

        last_post = self.all_posts[-1]

        self.assertEqual('About Me', last_post.title)
        self.assertEqual(4, last_post.id)
        self.assertEqual(self.datetime(2000, 2, 10, 1, 13, 17), last_post.created)
        self.assertEqual('My_Daily_Life', last_post.tag)
        self.assertEqual('''<h1>Jun Hyeok Lee</h1>
<h2>👋 Hello world!</h2>
<ul>
<li>Born on 2000/02/10</li>
<li>Male</li>
<li>Living in Pangyo, Bundang-gu, Gyeonggi-do, South Korea</li>
<li>Love playing Game, Guitar and coding!   </li>
</ul>
<hr />
<ul>
<li>한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )</li>
<li>대한민국 공군 ROKAF 병 825기 정보체계관리(30010 과정) (2..</li>
</ul>''', last_post.content_preview)

    # db input check
    def test_could_add_post_into_db(self):

        added_post = self.get_test_post()

        self.insert_post_at_db(added_post)

        self.assertEqual(self.get_test_post(), added_post)

        self.set_all_posts(self.Post.query.order_by(Post.created.desc()).all())
        all_posts = self.get_all_posts()
        
        self.assertEqual(5, len(all_posts))
        
        added_test_post = all_posts[-2]
        
        self.assertEqual('Test title for testing', added_test_post.title)
        self.assertEqual('IT', added_test_post.tag)
        self.assertEqual('<p>This is test content</p>', added_test_post.content)
        self.assertEqual('This is test content..', added_test_post.content_preview)

        last_post = all_posts[-1]

        self.assertEqual(4, last_post.id)
        
    # db delete check
    def test_could_delete_post_into_db(self):

        self.assertEqual(5, len(self.get_all_posts()))

        added_post = self.get_selected_post_by_title('Test title for testing')

        db.session.delete(added_post.first())

        self.set_all_posts(Post.query.order_by(Post.created.desc()).all())

        self.assertEqual(4, len(self.get_all_posts()))

        selected_post = self.get_all_posts()[-2]

        self.assertNotEqual('Test title for testing', selected_post.title)
        self.assertNotEqual('IT', selected_post.tag)
        self.assertNotEqual('<p>This is test content</p>', selected_post.content)
        self.assertNotEqual('This is test content..', selected_post.content_preview)

        self.assertEqual(3, selected_post.id)

    # db modifing check
    def test_could_modify_post_at_db(self):
        self.test_could_add_post_into_db()

        self.assertEqual(5, len(self.get_all_posts()))

        selected_post = self.get_selected_post_by_title('Test title for testing')
        new_content = 'This is new test content'
        new_content = markdown.markdown(new_content)

        self.assertEqual('<p>This is test content</p>', selected_post.first().content)

        selected_post.update(dict(content=new_content))

        selected_post = self.get_selected_post_by_title('Test title for testing').first()

        self.assertEqual(5, len(self.get_all_posts()))
        self.assertEqual('IT', selected_post.tag)
        self.assertEqual('<p>This is new test content</p>', selected_post.content)

        last_post = self.all_posts[-1]

        self.assertEqual(4, last_post.id)

    def tearDown(self):
        if os.path.exists('../Myblog_backend/app.db-journal'):
            print('delete journal file\n')
            os.remove('../Myblog_backend/app.db-journal')


class ModifingDB_Test(DB_Testcase_Root):
    from init_db import InitializeDB
    from update_db import UpdatePost

    import shutil

    TESTING = True

    # TODO: should write update_db testcases
    # 1. post deleted
    def test_should_update_deleted_post(self):

        self.make_new_post()

        self.UpdatePost()

        self.assertEqual(3, len(Post.query.filter_by(tag=self.category).all()))

        # remove post
        self.shutil.rmtree(self.test_folder)

        self.UpdatePost()

        self.assertEqual(4, Post.query.filter_by(title='About Me').first().id)
        self.assertEqual(2, len(Post.query.filter_by(tag=self.category).all()))

    # 2. post created
    def test_should_update_created_post(self):

        self.make_new_post()

        self.UpdatePost()

        self.assertEqual(5, len(Post.query.all()))

    # 3. post modified - modify title or content or content preview
    def test_should_update_modified_post_1(self):

        self.make_new_post()

        self.UpdatePost()

        new_post = Post.query.filter_by(title='This is Test title').first()

        self.assertEqual(5, new_post.id)
        self.assertEqual(4, Post.query.filter_by(title='About Me').first().id)


        modified_content = 'the content has modified!'

        self.make_file(os.path.join(self.test_folder, 'post.md'), modified_content)

        self.UpdatePost()

        new_post = Post.query.filter_by(title='This is Test title').first()

        self.assertEqual(5, new_post.id)
        self.assertEqual('<p>the content has modified!</p>', new_post.content)
    
    def tearDown(self):
        if self.os.path.exists(self.test_folder):
            self.shutil.rmtree(self.test_folder)

        self.UpdatePost()


class ModifingDB_Test_2(DB_Testcase_Root):
    # This testcase will cause DB instance mismatch, don't run at live environment!
    from init_db import InitializeDB
    from update_db import UpdatePost

    import shutil

    SQLALCHEMY_DATABASE_URI = "sqlite://" 
    TESTING = True

    # 3. post modified - modify category(tag)
    def test_should_update_modified_post_2(self):
        import shutil
        
        self.make_new_post()

        self.UpdatePost()

        new_post = Post.query.filter_by(title='This is Test title').first()

        self.assertEqual(5, new_post.id)
        self.assertEqual(4, Post.query.filter_by(title='About Me').first().id)

        source_files = os.listdir(self.test_folder)

        new_category = 'IT'
        new_category_folder = os.path.join(self.post_dir, new_category)
        new_post_folder = os.path.join(new_category_folder, self.test_created_folder)

        os.mkdir(new_category_folder)
        os.mkdir(new_post_folder)
        for file in source_files:
            shutil.move(os.path.join(self.test_folder, file), new_post_folder)
        shutil.rmtree(self.test_folder)

        self.UpdatePost()

        self.assertEqual(2, len(Post.query.filter_by(tag='Development').all()))
        self.assertEqual(1, len(Post.query.filter_by(tag='IT').all()))
        self.assertEqual(5, Post.query.filter_by(title='This is Test title').first().id)
        self.assertEqual(5, len(Post.query.all()))
        self.assertEqual('IT', Post.query.all()[-1].tag)

        if self.os.path.exists(new_category_folder):
            shutil.rmtree(new_category_folder)

    def tearDown(self):
        if self.os.path.exists(self.test_folder):
            self.shutil.rmtree(self.test_folder)


class InitDB_Test(DB_Testcase_Root):
    import init_db

    def test_could_get_posts(self):
        posts = Post.query.all()

        self.assertEqual(4, len(posts))
        
        for i in range(0, len(posts)):
            self.assertEqual(i+1, posts[i].id)

    def test_could_get_aboutme(self):
        from datetime import datetime
        
        aboutme_post = Post.query.filter_by(title="About Me").first()

        self.assertEqual("About Me", aboutme_post.title)
        self.assertEqual(datetime(2000, 2, 10, 1, 13, 17), aboutme_post.created)

    def test_should_read_double_filtering(self):
        post1 = Post.query.filter_by(title='About Me')

        post2 = post1.filter_by(tag='My_Daily_Life')

        self.assertEqual('About Me', post2.first().title)


class Util_Test(unittest.TestCase):
    
    def test_could_get_amout_of_posts_at_category_folder(self):
        post_dir = os.path.abspath('../Myblog_posts/posts')
        category_name_lists = os.listdir(post_dir)

        develop_category_folder = os.path.join(post_dir, 'Development')

        self.assertEqual(2, len(os.listdir(develop_category_folder)))
        print(os.listdir(develop_category_folder))

    def test_could_print_difference_of_two_lists(self):
        list1 = ['Test1', 'Test2', 'Test3']
        list2 = ['Test1']

        setlist1 = set(list1)
        setlist2 = set(list2)

        self.assertEqual(2, len(setlist1 - setlist2))
        self.assertEqual(0, len(list(setlist2 - setlist1)))

    def test_could_get_none_text_from_empty_txt_file(self):
        import os

        empty_text = None

        self.assertEqual(None, empty_text)
        self.assertNotEqual('', empty_text)
        with open('test.txt', 'wt') as f0:
            f0.close()
        with open('test.txt', 'r') as f:
            empty_text = f.read()
            os.remove('test.txt')
            f.close()
        
        self.assertEqual('', empty_text)
        self.assertNotEqual(None, empty_text)

    def test_could_get_filectime(self):
        import os, time

        post_dir = os.path.abspath('../Myblog_posts/posts')

        post_file = os.path.join(post_dir, 'Development/20220602062550/post.md')
        
        post_file_time = time.ctime(os.path.getmtime(post_file))
        
        with open(post_file, 'r') as f:
            file = f.tell()
            selected_post_file_time = os.path.getmtime(file)
            selected_post_file_time = time.ctime(selected_post_file_time)
            
        # return last commited date at Github (more exactly, it will return last pulled date at Github Origin)
        print('\nLast Commited Date from Github:', post_file_time)

        # return last file opened date at code
        print('\nLast File Opened Date from Local:', selected_post_file_time)

        # that two date will not same
        self.assertNotEqual(post_file_time, selected_post_file_time)


if __name__ == '__main__':
    unittest.main()

import unittest
from app.routes import *


def test_update_db():
    post_dir = os.path.abspath('../Myblog_posts/posts')
    dirname = os.path.dirname(post_dir)
    listdirname = os.listdir(post_dir)

    # variable lists:
    # IT, Study, Hobby, My_Daily_Life, Development, Game = \
    #     listdirname[0], listdirname[1], listdirname[2], listdirname[3], listdirname[4], listdirname[5]

    for cat_name in listdirname:
        post_dates = os.listdir(os.path.join(post_dir, cat_name))

    db_selected = Post.query.filter_by(tag=cat_name).all()
    db_dates = []
    for post in db_selected:
        db_dates.append(post.get_exact_created())

    for date in post_dates:
        year, month, day, hour, minute, sec = int(date[:4]), int(date[4:6]), int(date[6:8]),\
            int(date[8:10]), int(date[10:12]), int(date[12:14])
        new_date = datetime(year, month, day, hour, minute, sec)

        # checking and add newest posts at selected categories
        if str(new_date) not in db_dates:
            post_created = new_date
            with open(os.path.join(post_dir, cat_name, date, 'title.txt'), 'r') as f1:
                post_title = f1.read()
                f1.close()
            with open(os.path.join(post_dir, cat_name, date, 'post.md'), 'r') as f2:
                post_content = f2.read()
                f2.close()
            new_post = Post(title=post_title, content=post_content, created=post_created, tag=cat_name)
            db.session.add(new_post)


class Dotenv_Test(unittest.TestCase):
    
    def test_could_load_SECRET_KEY_from_env(self):
        from config import Config

        self.assertEqual('10308431c9df4dca98a308187f0c6b74', app.config['SECRET_KEY'])

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

#     def test_could_save_converted_text_in_DB(self):
#         from datetime import datetime

#         # converted_text = markdown.markdown(self.long_md_text)
#         content = self.long_md_text
#         title = 'Test title'
#         date, time = (datetime.today().isoformat(timespec='seconds')).split('T')
#         time_now = f'{date} {time}'

#         # insert new DB instance which content is converted long markdown text.
#         self.conn.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content,))
        
#         db_notes = self.conn.execute('SELECT id, title, created, content FROM notes;').fetchall()
#         notes = []
#         for note in db_notes:
#             note = dict(note)
#             note['content'] = markdown.markdown(note['content'])
#             notes.append(note)

#         self.assertEqual('''<h2>👋 Hello world!</h2>
# <ul>
# <li>한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )</li>
# <li>대한민국 공군 ROKAF 병 825기 정보체계관리(30010 과정) (2021.04.12 ~ 2023.01.11)</li>
# <li>GiftMusic backend 개발자 (2020.09 ~ 2021.04)</li>
# </ul>''', notes[-1]['content'])

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


class Database_Test(unittest.TestCase):
    from app.models import Post
    from app import db

    def setUp(self):

        posts = Post.query.all()

        self.posts = Post.query.order_by(Post.created.desc()).all()

    def test_could_get_db(self):

        title_1 = 'The First Title' 
        tag_1 = 'IT' 
        content_1 = '# test content1' 
        title_2 = 'Another title' 
        tag_2 = 'My_Daily_Life' 
        content_2 = '_test content2_' 
        title_3 = 'Test Title' 
        tag_3 = 'Hobby' 
        content_3 = 'Visit [this page](https://www.digitalocean.com/community/tutorials) for more tutorials.'

        content_1 = markdown.markdown(content_1) 
        content_2 = markdown.markdown(content_2) 
        content_3 = markdown.markdown(content_3)

        post_1 = self.Post(title=title_1, content=content_1, tag=tag_1) 
        self.db.session.add(post_1) 
        post_2 = self.Post(title=title_2, content=content_2, tag=tag_2) 
        self.db.session.add(post_2) 
        post_3 = self.Post(title=title_3, content=content_3, tag=tag_3) 
        self.db.session.add(post_3)

        self.posts = Post.query.all()

        from datetime import datetime
        time = datetime(2022, 5, 28, 13, 47, 42, 526501)


        selected_post = self.posts[1]

        self.assertEqual(('The First Title', '<h1>test content1</h1>', 'IT'), (selected_post.title, selected_post.content, selected_post.tag))

        print('all self posts:',self.posts)

        for post in self.posts:
            print('title:', post.title)
            print('created:', post.get_created())
        
        self.db.session.delete(post_1)
        self.db.session.delete(post_2)
        self.db.session.delete(post_3)
    
    def test_could_found_about_me_post(self):
        about_me = Post.query.filter_by(title='About Me').first()

        self.assertEqual('About Me', about_me.title)
    
    # def test_could_update_new_posts(self):

    #     print('self post:', self.Post.query.all())
    #     self.assertEqual(1, len(self.Post.query.all()))

    #     # should update 2 posts
    #     test_update_db()
    #     print('updated posts:', self.Post.query.all())
    #     self.assertEqual(3, len(self.Post.query.all()))

    #     # should not update any posts
    #     test_update_db()
    #     print('updated posts(2):', self.Post.query.all())
    #     self.assertEqual(3, len(self.Post.query.all()))

    def test_could_delete_query(self):
        pass


class ServerTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

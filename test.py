import unittest
# from flask_app import *
from app.routes import *


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
        self.posts = Post.query.order_by(Post.created.desc()).all()

    def test_could_get_db(self):
        from datetime import datetime
        time = datetime(2022, 5, 28, 13, 47, 42, 526501)

        selected_post = self.posts[3]

        self.assertEqual(4, len(self.posts))
        self.assertEqual(('The First Title', '<h1>test content1</h1>', 'IT'), (selected_post.title, selected_post.content, selected_post.tag))

        for post in self.posts:
            print(post.title)
            print(post.get_created())
    
    def test_could_found_about_me_post(self):
        about_me = Post.query.filter_by(title='About Me').first()

        self.assertEqual('About Me', about_me.title)
    
    def test_could_found_categoried_posts(self):
        posts = Post.query.filter_by(tag='IT').all()

        self.assertEqual(1, len(posts))
        self.assertEqual('The First Title', posts[0].title)

    def test_could_delete_query(self):
        pass


class Fetching_Post(unittest.TestCase):
    
    def could_read_post(self):
        import datetime

        # post_dir = os.path.abspath('../Myblog_posts/posts')
        # Development = post_dir.__getitem__('Development')
        # print(Development)
        print('this is date')
        '/home/bnbong/programming/projects/Myblog_posts/posts/Development/202012280018/post.md'


class ServerTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

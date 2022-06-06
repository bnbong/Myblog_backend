import unittest
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

        content_1_preview = content_1[:300]
        content_2_preview = content_2[:300]
        content_3_preview = content_3[:300]
        content_1 = markdown.markdown(content_1) 
        content_2 = markdown.markdown(content_2) 
        content_3 = markdown.markdown(content_3)

        post_1 = self.Post(title=title_1, content=content_1, content_preview=content_1_preview, tag=tag_1) 
        self.db.session.add(post_1) 
        post_2 = self.Post(title=title_2, content=content_2, content_preview=content_2_preview, tag=tag_2) 
        self.db.session.add(post_2) 
        post_3 = self.Post(title=title_3, content=content_3, content_preview=content_3_preview, tag=tag_3) 
        self.db.session.add(post_3)

        self.posts = Post.query.all()

        from datetime import datetime
        time = datetime(2022, 5, 28, 13, 47, 42, 526501)


        selected_post = self.posts[-3]

        self.assertEqual(('The First Title', '<h1>test content1</h1>', 'IT'), (selected_post.title, selected_post.content, selected_post.tag))

        for post in self.posts:
            print('\ntitle:', post.title)
            print('\ncreated:', post.get_created())
        
        self.db.session.delete(post_1)
        self.db.session.delete(post_2)
        self.db.session.delete(post_3)

        if os.path.exists('app.db-journal'):
            os.remove('app.db-journal')

    def test_could_get_about_me(self):
        pass


class InitDBTest(unittest.TestCase):
    import init_db

    def test_could_get_posts(self):
        posts = Post.query.all()

        self.assertEqual(4, len(posts))

    def test_could_get_aboutme(self):
        from datetime import datetime
        
        aboutme_post = Post.query.filter_by(title="About Me").first()

        self.assertEqual("About Me", aboutme_post.title)
        self.assertEqual(datetime(2000, 2, 10, 1, 13, 17), aboutme_post.created)

class UtilTest(unittest.TestCase):
    
    def setUp(self):
        import os

        with open('test.txt','wt') as f0:
            f0.close()

    def test_could_get_none_text_from_empty_txt_file(self):
        import os

        empty_text = None

        self.assertEqual(None, empty_text)
        self.assertNotEqual('', empty_text)
        
        with open('test.txt', 'rt') as f:
            empty_text = f.read()
            f.close()
        
        self.assertEqual('', empty_text)
        self.assertNotEqual(None, empty_text)

        if os.path.exists('test.txt'):
            os.remove('test.txt')

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


class ServerTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

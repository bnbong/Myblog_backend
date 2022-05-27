import unittest
from flask_app import *
# from flask_testing import TestCase

class Fetching_notes_DBTest(unittest.TestCase):

    def setUp(self):
        conn = get_db_connection()
        db_notes = conn.execute('SELECT id, title, created, content FROM notes;').fetchall()
        conn.close()
        self.db_notes = db_notes

        self.notes = []
        for self.note in self.db_notes:
            self.note = dict(self.note)
            self.note['content'] = markdown.markdown(self.note['content'])
            self.notes.append(self.note)

    def test_could_db_connection(self):
        assert self.db_notes is not None

    def test_could_get_right_db_indexes(self):
        assert self.notes is not None
        print(self.notes)

        self.assertEqual(1, (self.notes[0])['id'])
        self.assertEqual(2, (self.notes[1])['id'])
        self.assertEqual(3, (self.notes[2])['id'])

    def test_could_not_get_db_connection(self):
        with self.assertRaises(sqlite3.OperationalError) as context:
            conn2 = sqlite3.connect('~/database.db')
            conn2.row_factory = sqlite3.Row
            db_notes2 = conn2.execute('SELECT id, title, created, content FROM notes;').fetchall()
            conn2.close()
        
        # If this test case failed, the python compiler found right sqlite3 database at '~/Myblog_backend/database.db'
        self.assertEqual("unable to open database file", context.exception.__str__())


class Modify_notes_DBTest(unittest.TestCase):

    def setUp(self):
        conn = get_db_connection()
        db_notes = conn.execute('SELECT id, title, created, content FROM notes;').fetchall()
        conn.close()
        self.db_notes = db_notes

        self.notes = []
        for self.note in self.db_notes:
            self.note = dict(self.note)
            self.note['content'] = markdown.markdown(self.note['content'])
            self.notes.append(self.note)

    def test_could_insert_aboutme_to_DB(self):
        from datetime import datetime

        title = "About Me"
        content = """
    ![header](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=300&section=header&text=JunHyeok%20Lee&fontSize=90&animation=fadeIn)

![Most Used Language](https://github-readme-stats.vercel.app/api/top-langs/?username=bnbong)

## 👋 Hello world!

 - 한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )
 - 대한민국 공군 ROKAF 병 825기 정보체계관리(30010 과정) (2021.04.12 ~ 2023.01.11)
 - GiftMusic backend 개발자 (2020.09 ~ 2021.04)
        """
        date, time = (datetime.today().isoformat(timespec='seconds')).split('T')
        time_now = f'{date} {time}'
        self.notes.append(
            {"id":4, 
            "title":"About Me", 
            "created":time_now, 
            "content":content}
            )
        
        self.assertEqual(self.notes.__len__(), 4)
        self.assertEqual(self.notes[3].get('title'), "About Me")
        
    def test_could_change_note_title(self):
        pass

    def test_could_change_note_content(self):
        self.another_conn = get_db_connection()
        another_id_from_db = self.another_conn.execute('SELECT id FROM notes WHERE id = 2;').fetchone()['id']

        self.assertEqual(2, (self.notes[1])['id'])
        self.assertEqual(2, another_id_from_db)
        self.assertEqual('Another note', (self.notes[1])['title'])

        new_content = 'Hello World!'

        self.another_conn.execute('UPDATE notes SET content = ? WHERE id = ?', (new_content, another_id_from_db))
        another_item = self.another_conn.execute('SELECT id, title, created, content FROM notes WHERE id = 2;').fetchall()
        self.another_conn.close()

        self.assertEqual('Hello World!', (another_item[0])['content'])
        self.assertNotEqual((self.notes[1])['content'], (another_item[0])['content'])
        
    def test_could_delete_note(self):
        self.another_conn_2 = get_db_connection()
        another_id_from_db_2 = self.another_conn_2.execute('SELECT id FROM notes WHERE id = 3;').fetchone()['id']

        self.assertEqual(3, (self.notes[2])['id'])
        self.assertEqual('<p>Visit <a href="https://www.digitalocean.com/community/tutorials">this page</a> for more tutorials.</p>',
         (self.notes[2])['content'])

        self.another_conn_2.execute('DELETE FROM notes WHERE id = ?;', (another_id_from_db_2,))

        another_db_notes = self.another_conn_2.execute('SELECT id, title, created, content FROM notes;').fetchall()
        another_notes = []
        for note in another_db_notes:
            note = dict(note)
            another_notes.append(note)
            
        self.assertEqual(2, len(another_notes))
        self.assertNotEqual('<p>Visit <a href="https://www.digitalocean.com/community/tutorials">this page</a> for more tutorials.</p>',
         (another_notes[-1])['content'])
        self.assertEqual('Another note', (another_notes[-1])['title'])


class Fetching_comment_DBTEST(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_could_db_connection(self):
        pass


# class FetchingFrontend(TestCase):

#     @app.route('/')
#     def test_make_page(self):
#         client = Flask(__name__, template_folder='Myblog_frontend/templates')
#         render_template('index.html', notes=[])

#     def test_get_template_from_another_directory(self):
#         response = self.client.get('/')

#         self.assert_template_used('index.html')



class ServerTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

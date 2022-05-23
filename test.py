import unittest
from flask_app import *
from flask_testing import TestCase

class DBTest(unittest.TestCase):

    def setUp(self):
        conn = get_db_connection()
        db_notes = conn.execute('SELECT id, created, content FROM notes;').fetchall()
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

        self.assertEqual(1, (self.notes[0])['id'])
        self.assertEqual(2, (self.notes[1])['id'])
        self.assertEqual(3, (self.notes[2])['id'])

    def test_could_not_get_db_connection(self):
        with self.assertRaises(sqlite3.OperationalError) as context:
            conn2 = sqlite3.connect('~/database.db')
            conn2.row_factory = sqlite3.Row
            db_notes2 = conn2.execute('SELECT id, created, content FROM notes;').fetchall()
            conn2.close()
        
        # If this test case failed, the python compiler found right sqlite3 database at '~/Myblog_backend/database.db'
        self.assertEqual("unable to open database file", context.exception.__str__())


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

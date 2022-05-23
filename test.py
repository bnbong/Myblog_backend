import unittest
from flask_app import *

class DBTest(unittest.TestCase):

    def setUp(self):
        conn = get_db_connection()
        db_notes = conn.execute('SELECT id, created, content FROM notes;').fetchall()
        conn.close()
        self.db_notes = db_notes

    def test_db_connection(self):
        assert self.db_notes is not None

    def test_get_db_indexes(self):
        notes = []
        for note in self.db_notes:
            note = dict(note)
            note['content'] = markdown.markdown(note['content'])
            notes.append(note)

        print(notes)
    

class ServerTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

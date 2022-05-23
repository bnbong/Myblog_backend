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

        assert notes is not None

    def test_could_not_get_db_connection(self):
        with self.assertRaises(sqlite3.OperationalError) as context:
            conn2 = sqlite3.connect('~/database.db')
            conn2.row_factory = sqlite3.Row
            db_notes2 = conn2.execute('SELECT id, created, content FROM notes;').fetchall()
            conn2.close()
        
        # If this test case failed, the python compiler found right sqlite3 database at '~/Myblog_backend/database.db'
        self.assertEqual("unable to open database file", context.exception.__str__())


class ServerTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

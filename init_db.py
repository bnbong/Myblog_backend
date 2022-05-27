# init test data for example view

import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO notes (title, content) VALUES (?, ?)", ('The First Note', '# test content1',))
cur.execute("INSERT INTO notes (title, content) VALUES (?, ?)", ('Another note', '_test content2_',))
cur.execute("INSERT INTO notes (title, content) VALUES (?, ?)", ('Test Title', 'Visit [this page](https://www.digitalocean.com/community/tutorials) for more tutorials.',))

connection.commit()
connection.close()
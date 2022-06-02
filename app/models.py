# make models.py for use pagination -> convert db query using schema.sql
from app import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(125))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String())
    content_preview = db.Column(db.String(300))
    tag = db.Column(db.String(200))

    def __repr__(self): 
        return '<Post {}>'.format(self.title)

    def all(self):
        return (self.id, self.title, self.created, self.content, self.content_preview, self.tag)

    def get_created(self):
        return self.created.strftime("%c")

    def get_exact_created(self):
        return self.created.strftime("%Y-%m-%d %X")
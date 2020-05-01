from config.db import db
from datetime import datetime

class Project(db.Document):
    name = db.StringField(required=True, unique=True)
    createdAt = db.DateTimeField(
        default=datetime.now(), help_text='date the student was created')
    updatedAt = db.DateTimeField()

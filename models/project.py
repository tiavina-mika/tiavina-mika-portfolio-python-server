from config.db import db
from datetime import datetime

class Project(db.Document):
    name = db.StringField(required=True)
    slug = db.StringField(required=True, unique=True)
    createdAt = db.DateTimeField(default=datetime.now())
    updatedAt = db.DateTimeField()


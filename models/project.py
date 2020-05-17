from config.db import db
from datetime import datetime

class Project(db.Document):
    name = db.StringField(required=True)
    slug = db.StringField(required=True, unique=True)
    tags = db.ListField(db.StringField())
    createdAt = db.DateTimeField(default=datetime.now())
    updatedAt = db.DateTimeField()
    image = db.StringField()
    _image_file = db.FileField()


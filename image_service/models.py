import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Image(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    prompt = db.Column(db.Text)
    image_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    def __init__(self, prompt, image_url):
        self.id = f"id_{uuid.uuid4()}"
        self.prompt = prompt
        self.image_url = image_url
        self.created_at = datetime.utcnow()

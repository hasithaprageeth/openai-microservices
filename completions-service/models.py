import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Completion(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    prompt = db.Column(db.Text)
    completed_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    def __init__(self, prompt, completed_text):
        self.id = f"id_{uuid.uuid4()}"
        self.prompt = prompt
        self.completed_text = completed_text
        self.created_at = datetime.utcnow()

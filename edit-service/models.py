import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Edit(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    instruction = db.Column(db.Text)
    prompt = db.Column(db.Text)
    edited_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    def __init__(self, instruction, prompt, edited_text):
        self.id = f"id_{uuid.uuid4()}"
        self.instruction = instruction
        self.prompt = prompt
        self.edited_text = edited_text
        self.created_at = datetime.utcnow()

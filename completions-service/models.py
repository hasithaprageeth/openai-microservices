import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Chat(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    request_role = db.Column(db.String(10))
    prompt = db.Column(db.Text)
    response_role = db.Column(db.String(10))
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    def __init__(self, request_role, prompt, response_role, response):
        self.id = f"id_{uuid.uuid4()}"
        self.request_role = request_role
        self.prompt = prompt
        self.response_role = response_role
        self.response = response
        self.created_at = datetime.utcnow()

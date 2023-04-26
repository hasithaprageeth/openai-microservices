from app import db


class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Text, primary_key=True)
    request_role = db.Column(db.Text)
    prompt = db.Column(db.Text)
    response_role = db.Column(db.Text)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())


# Create table if it doesn't exist
db.create_all()

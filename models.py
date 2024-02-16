from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class SpeakingTest(db.Model):
    __tablename__ = 'speaking_test'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, nullable=False)
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    used_time = db.Column(db.Integer, default=0, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    # Fields for Questions
    for i in range(1, 11):
        locals()[f'question{i}_part1'] = db.Column(db.String(100), nullable=False if i <= 4 else True)
        locals()[f'question{i}_part2'] = db.Column(db.String(100), nullable=False if i <= 4 else True)
        locals()[f'question{i}_part3'] = db.Column(db.String(100), nullable=False if i <= 4 else True)

    # Fields for Thinking and Speaking Times for each part
    for i in range(1, 11):
        locals()[f'thinking{i}_part1'] = db.Column(db.Integer, nullable=True)
        locals()[f'speaking{i}_part1'] = db.Column(db.Integer, nullable=True)

        locals()[f'thinking{i}_part3'] = db.Column(db.Integer, nullable=True)
        locals()[f'speaking{i}_part3'] = db.Column(db.Integer, nullable=True)

    locals()['thinking_part2'] = db.Column(db.Integer, nullable=True)
    locals()['speaking_part2'] = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'SpeakingTest(id={self.id}, chat_id={self.chat_id}, is_private={self.is_private})'


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_premium = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    chat_id = db.Column(db.Integer, nullable=False)
    education_center = db.Column(db.String, nullable=False)
    verification = db.Column(db.Integer, nullable=False)
    payment = db.Column(db.String(1000000), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'USER -> id: {self.id}, chat_id: {self.chat_id}, name: {self.name}'


class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(1000000), nullable=False)
    is_premium = db.Column(db.Integer, default=False, nullable=False)
    chat_id = db.Column(db.Integer, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    limit = db.Column(db.Integer, nullable=True)  # Adjust based on your requirements
    used_time = db.Column(db.Integer, default=0, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    question_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'TokenUsage(id={self.id}, chat_id={self.chat_id}, token={self.token}'


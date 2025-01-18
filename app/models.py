from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # type will be multiple_choice or text_input
    correct_answer = db.Column(db.String(200), nullable=False)
    options = db.Column(db.String(500), nullable=True)  #multiple choices

    def get_options(self):
        if self.options:
            return self.options.split(',')
        return None
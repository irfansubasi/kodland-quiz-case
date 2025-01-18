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
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scores = db.relationship('Score', backref='student', lazy=True)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)

    @property
    def percentage(self):
        return (self.score / self.total_questions) * 100 if self.total_questions > 0 else 0

    @classmethod
    def get_highest_score(cls, student_id):
        highest = cls.query.filter_by(student_id=student_id)\
            .order_by(desc(cls.score))\
            .first()
        
        if highest is None:
            
            default_score = cls(
                student_id=student_id,
                score=0,
                total_questions=Question.query.count() or 1
            )
            return default_score
            
        return highest
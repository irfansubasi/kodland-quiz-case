from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import db, Student, Score, Question

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        if student_name:

            student = Student.query.filter_by(name=student_name).first()
            if not student:
                student = Student(name=student_name)
                db.session.add(student)
                db.session.commit()
            
            session['student_id'] = student.id
            session['student_name'] = student_name
            return redirect(url_for('main.quiz'))
        
    return render_template('index.html')


@bp.route('/quiz')
def quiz():
    if 'student_id' not in session:
        return redirect(url_for('main.index'))
    
    student_id = session['student_id']
    student_name = session['student_name']
    highest_score = Score.get_highest_score(student_id)
    questions = Question.query.all()
    
    return render_template('quiz.html',
                         student_name=student_name,
                         questions=questions,
                         highest_score=highest_score)
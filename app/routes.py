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

@bp.route('/submit', methods=['POST'])
def submit_quiz():
    if 'student_id' not in session:
        return redirect(url_for('main.index'))

    questions = Question.query.all()
    total_questions = len(questions)
    score = 0
    answers = []
    
    for question in questions:
        user_answer = request.form.get(f'answer_{question.id}', '').strip()
        correct_answer = question.correct_answer.strip()
        
        if question.question_type == 'text_input':
            is_correct = user_answer.lower() == correct_answer.lower()
        else:
            is_correct = user_answer == correct_answer
            
        if is_correct:
            score += 1
            
        answers.append({
            'question': question.question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'question_type': question.question_type
        })
    
    new_score = Score(
        student_id=session['student_id'],
        score=score,
        total_questions=total_questions
    )
    db.session.add(new_score)
    db.session.commit()

    highest_score = Score.get_highest_score(session['student_id'])
    
    return render_template('result.html',
                         student_name=session['student_name'],
                         score=score,
                         total=total_questions,
                         percentage=(score/total_questions)*100,
                         answers=answers,
                         highest_score=highest_score)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import db, Student

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
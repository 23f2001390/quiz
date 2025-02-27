from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import or_, func
from collections import defaultdict

from models import db
from models.user import User
from models.quiz import Subject, Chapter, Quiz, Question
from models.score import Score
from forms.admin import SubjectForm, ChapterForm, QuizForm, QuestionForm, AdminSearchForm
from models.chart_data import ChartData

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/dashboard')
@admin_required
def dashboard():
    subjects = Subject.query.all()
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/dashboard.html', subjects=subjects, users=users)

# Subject CRUD
@admin.route('/subject/new', methods=['GET', 'POST'])
@admin_required
def create_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject created successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/subject_form.html', form=form, title='New Subject')

@admin.route('/subject/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    form = SubjectForm(obj=subject)
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/subject_form.html', form=form, title='Edit Subject')

@admin.route('/subject/<int:id>/delete')
@admin_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# Chapter CRUD
@admin.route('/subject/<int:subject_id>/chapter/new', methods=['GET', 'POST'])
@admin_required
def create_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = ChapterForm()
    if form.validate_on_submit():
        chapter = Chapter(
            subject_id=subject_id,
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter created successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/chapter_form.html', form=form, subject=subject, title='New Chapter')

@admin.route('/chapter/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    form = ChapterForm(obj=chapter)
    if form.validate_on_submit():
        chapter.name = form.name.data
        chapter.description = form.description.data
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/chapter_form.html', form=form, subject=chapter.subject, title='Edit Chapter')

@admin.route('/chapter/<int:id>/delete')
@admin_required
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# Quiz CRUD
@admin.route('/chapter/<int:chapter_id>/quiz/new', methods=['GET', 'POST'])
@admin_required
def create_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    form = QuizForm()
    if form.validate_on_submit():
        total_duration = (form.duration_hours.data * 60) + form.duration_minutes.data
        quiz = Quiz(
            chapter_id=chapter.id,
            title=form.title.data,
            description=form.description.data,
            date_of_quiz=form.date_of_quiz.data,
            duration_minutes=total_duration
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('admin.view_quiz', id=quiz.id))
    return render_template('admin/quiz_form.html', form=form, chapter=chapter, title='New Quiz')

@admin.route('/quiz/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    form = QuizForm(obj=quiz)
    
    if request.method == 'GET':
        # Split duration into hours and minutes for form
        form.duration_hours.data = quiz.duration_minutes // 60
        form.duration_minutes.data = quiz.duration_minutes % 60
    
    if form.validate_on_submit():
        total_duration = (form.duration_hours.data * 60) + form.duration_minutes.data
        quiz.title = form.title.data
        quiz.description = form.description.data
        quiz.date_of_quiz = form.date_of_quiz.data
        quiz.duration_minutes = total_duration
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('admin.view_quiz', id=quiz.id))
    return render_template('admin/quiz_form.html', form=form, chapter=quiz.chapter, title='Edit Quiz')

@admin.route('/quiz/<int:id>/delete')
@admin_required
def delete_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# Question CRUD
@admin.route('/quiz/<int:quiz_id>/question/new', methods=['GET', 'POST'])
@admin_required
def create_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            quiz_id=quiz_id,
            question_text=form.question_text.data,
            option_1=form.option_1.data,
            option_2=form.option_2.data,
            option_3=form.option_3.data,
            option_4=form.option_4.data,
            correct_option=form.correct_option.data
        )
        db.session.add(question)
        db.session.commit()
        flash('Question created successfully!', 'success')
        return redirect(url_for('admin.view_quiz', id=quiz_id))
    return render_template('admin/question_form.html', form=form, quiz=quiz, title='New Question')

@admin.route('/question/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_question(id):
    question = Question.query.get_or_404(id)
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        question.question_text = form.question_text.data
        question.option_1 = form.option_1.data
        question.option_2 = form.option_2.data
        question.option_3 = form.option_3.data
        question.option_4 = form.option_4.data
        question.correct_option = form.correct_option.data
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('admin.view_quiz', id=question.quiz_id))
    return render_template('admin/question_form.html', form=form, quiz=question.quiz, title='Edit Question')

@admin.route('/question/<int:id>/delete')
@admin_required
def delete_question(id):
    question = Question.query.get_or_404(id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('admin.view_quiz', id=quiz_id))

# View specific quiz with its questions
@admin.route('/quiz/<int:id>')
@admin_required
def view_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    now = datetime.utcnow()
    return render_template('admin/view_quiz.html', quiz=quiz, now=now)

# User management
@admin.route('/users')
@admin_required
def list_users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/<int:id>/delete', methods=['POST'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.is_admin:
        flash('Cannot delete admin user.', 'danger')
        return redirect(url_for('admin.list_users'))
    
    # Delete associated scores
    Score.query.filter_by(user_id=user.id).delete()
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.list_users'))

@admin.route('/search', methods=['GET', 'POST'])
@admin_required
def search():
    form = AdminSearchForm()
    results = []
    
    if form.validate_on_submit():
        search_query = form.search_query.data
        search_type = form.search_type.data
        
        if search_type == 'users':
            results = User.query.filter(
                or_(
                    User.username.ilike(f'%{search_query}%'),
                    User.email.ilike(f'%{search_query}%')
                )
            ).all()
        elif search_type == 'subjects':
            results = Subject.query.filter(
                Subject.name.ilike(f'%{search_query}%')
            ).all()
        elif search_type == 'quizzes':
            results = Quiz.query.filter(
                or_(
                    Quiz.title.ilike(f'%{search_query}%'),
                    Quiz.description.ilike(f'%{search_query}%')
                )
            ).all()
        elif search_type == 'questions':
            results = Question.query.filter(
                or_(
                    Question.text.ilike(f'%{search_query}%'),
                    Question.explanation.ilike(f'%{search_query}%')
                )
            ).all()
    
    return render_template('admin/search.html', form=form, results=results)

@admin.route('/statistics')
@admin_required
def statistics():
    # Overall statistics
    total_users = User.query.filter_by(is_admin=False).count()
    total_quizzes = Quiz.query.count()
    total_attempts = Score.query.count()
    
    # Subject-wise top scores
    subjects = Subject.query.all()
    subject_stats = {
        'labels': [],
        'scores': []
    }
    
    for subject in subjects:
        top_scores = []
        for chapter in subject.chapters:
            for quiz in chapter.quizzes:
                # Safely calculate scores
                valid_scores = [
                    (s.score / s.total_questions * 100)
                    for s in quiz.scores
                    if s.total_questions > 0  # Only include scores where total_questions > 0
                ]
                if valid_scores:  # Only append if there are valid scores
                    top_scores.append(max(valid_scores))
        
        if top_scores:  # Only include subject if it has valid scores
            subject_stats['labels'].append(subject.name)
            subject_stats['scores'].append(round(max(top_scores), 2))
    
    # Subject-wise user attempts (concentric circles)
    attempt_stats = {
        'labels': subject_stats['labels'],  # Use same subjects
        'data': []  # Will contain [total_users, users_attempted, completed_all] for each subject
    }
    
    total_user_count = User.query.filter_by(is_admin=False).count()
    
    for subject in subjects:
        if subject.name in subject_stats['labels']:
            # Get all quizzes for this subject
            subject_quizzes = [quiz for chapter in subject.chapters for quiz in chapter.quizzes]
            
            # Users who attempted at least one quiz in this subject
            users_attempted = db.session.query(Score.user_id.distinct())\
                .join(Quiz)\
                .join(Chapter)\
                .filter(Chapter.subject_id == subject.id)\
                .count()
            
            # Users who completed all quizzes in this subject
            if subject_quizzes:
                users_completed = db.session.query(Score.user_id)\
                    .join(Quiz)\
                    .join(Chapter)\
                    .filter(Chapter.subject_id == subject.id)\
                    .group_by(Score.user_id)\
                    .having(func.count(Score.id) == len(subject_quizzes))\
                    .count()
            else:
                users_completed = 0
            
            attempt_stats['data'].append([
                total_user_count,      # Total users (outer circle)
                users_attempted,       # Users who attempted (middle circle)
                users_completed        # Users who completed all (inner circle)
            ])
    
    # Generate chart configurations
    top_scores_chart_config = ChartData.get_admin_top_scores_config(subject_stats)
    attempts_chart_config = ChartData.get_admin_attempts_config(attempt_stats)
    
    return render_template('admin/statistics.html',
                         total_users=total_users,
                         total_quizzes=total_quizzes,
                         total_attempts=total_attempts,
                         top_scores_chart_config=top_scores_chart_config,
                         attempts_chart_config=attempts_chart_config) 
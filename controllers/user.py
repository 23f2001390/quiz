from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import and_, or_

from models import db
from models.quiz import Subject, Quiz, Question, Chapter
from models.score import Score
from forms.quiz import QuizAttemptForm
from forms.user import UserSearchForm
from quiz_utils import QuizTimer, format_time
from chart_utils import ChartData

user = Blueprint('user', __name__, url_prefix='/user')

def user_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            flash('Access denied.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@user.route('/dashboard')
@user_required
def dashboard():
    # Get all subjects with their chapters and upcoming quizzes
    subjects = Subject.query.all()
    current_time = datetime.utcnow()
    
    # Get user's completed quizzes
    completed_quizzes = Score.query.filter_by(user_id=current_user.id).all()
    completed_quiz_ids = [score.quiz_id for score in completed_quizzes]
    
    return render_template('user/dashboard.html', 
                         subjects=subjects,
                         current_time=current_time,
                         completed_quiz_ids=completed_quiz_ids)

@user.route('/quiz/<int:id>')
@user_required
def view_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    current_time = datetime.utcnow()
    
    # Check if quiz is available
    if current_time > quiz.date_of_quiz:
        flash('This quiz has already ended.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    # Check if user has already attempted this quiz
    existing_score = Score.query.filter_by(
        user_id=current_user.id,
        quiz_id=quiz.id
    ).first()
    
    if existing_score:
        return redirect(url_for('user.view_quiz_attempt', quiz_id=quiz.id))
    
    return render_template('user/view_quiz.html', quiz=quiz)

@user.route('/quiz/<int:quiz_id>/attempt', methods=['GET', 'POST'])
@user_required
def attempt_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Check if quiz has already been attempted
    existing_score = Score.query.filter_by(user_id=current_user.id, quiz_id=quiz_id).first()
    if existing_score:
        flash('You have already attempted this quiz.', 'warning')
        return redirect(url_for('user.view_quiz_attempt', quiz_id=quiz_id))
    
    # Check if quiz is available
    if datetime.now() < quiz.date_of_quiz:
        flash('This quiz is not yet available.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    form = QuizAttemptForm()
    
    if request.method == 'GET':
        # Start the quiz timer
        QuizTimer.start_quiz(quiz_id, quiz.duration_minutes)
    
    if form.validate_on_submit() or QuizTimer.is_time_up(quiz_id):
        # Calculate score
        score = 0
        for question in quiz.questions:
            answer = request.form.get(f'answer_{question.id}')
            if answer and int(answer) == question.correct_option:
                score += 1
        
        # Record the score
        time_taken = QuizTimer.get_time_taken(quiz_id)
        quiz_score = Score(
            user_id=current_user.id,
            quiz_id=quiz_id,
            score=score,
            total_questions=quiz.questions.count(),
            time_taken=time_taken
        )
        db.session.add(quiz_score)
        db.session.commit()
        
        # Clear timer data
        QuizTimer.clear_timer(quiz_id)
        
        # If it's an AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'redirect_url': url_for('user.dashboard')
            })
        
        return redirect(url_for('user.quiz_result', id=quiz_id))
    
    # Get remaining time
    seconds_remaining = QuizTimer.get_remaining_time(quiz_id)
    if seconds_remaining <= 0:
        # Auto-submit if time is up
        return redirect(url_for('user.attempt_quiz', quiz_id=quiz_id))
    
    return render_template('user/attempt_quiz.html', 
                         quiz=quiz, 
                         form=form,
                         seconds_remaining=seconds_remaining,
                         time_display=format_time(seconds_remaining))

@user.route('/quiz/<int:quiz_id>/view_attempt')
@user_required
def view_quiz_attempt(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    score = Score.query.filter_by(user_id=current_user.id, quiz_id=quiz_id).first_or_404()
    questions = quiz.questions.all()
    return render_template('user/view_quiz_attempt.html', quiz=quiz, score=score, questions=questions)

@user.route('/quiz/<int:id>/result')
@user_required
def quiz_result(id):
    quiz = Quiz.query.get_or_404(id)
    score = Score.query.filter_by(
        user_id=current_user.id,
        quiz_id=quiz.id
    ).first_or_404()
    
    return render_template('user/quiz_result.html', quiz=quiz, score=score)

@user.route('/scores')
@user_required
def view_scores():
    scores = Score.query.filter_by(user_id=current_user.id).all()
    
    # Calculate basic statistics
    total_quizzes = len(scores)
    total_score = sum(score.score for score in scores)
    total_questions = sum(score.total_questions for score in scores)
    
    # Safely calculate average score
    average_score = 0
    if total_questions > 0:
        average_score = (total_score / total_questions) * 100
    
    # Safely calculate highest score
    highest_score = 0
    if scores:
        valid_scores = [(score.score / score.total_questions * 100) 
                       for score in scores 
                       if score.total_questions > 0]
        if valid_scores:
            highest_score = max(valid_scores)
    
    # Subject-wise quiz counts
    subject_stats = {}
    for score in scores:
        subject_name = score.quiz.chapter.subject.name
        if subject_name not in subject_stats:
            subject_stats[subject_name] = 1
        else:
            subject_stats[subject_name] += 1
    
    subject_chart = {
        'labels': list(subject_stats.keys()),
        'data': list(subject_stats.values())
    }
    
    # Month-wise attempts
    current_month = datetime.utcnow().month
    month_stats = {
        'labels': [],
        'data': []
    }
    
    # Get attempts for last 3 months
    for i in range(3):
        month = (current_month - i) if (current_month - i) > 0 else (12 + current_month - i)
        month_name = datetime.strptime(str(month), "%m").strftime("%B")
        month_attempts = len([s for s in scores if s.attempted_at.month == month])
        
        month_stats['labels'].append(month_name)
        month_stats['data'].append(month_attempts)
    
    # Generate chart configurations
    subject_chart_config = ChartData.get_subject_chart_config(subject_chart)
    month_chart_config = ChartData.get_month_chart_config(month_stats)
    
    return render_template('user/scores.html',
                         scores=scores,
                         total_quizzes=total_quizzes,
                         total_score=total_score,
                         total_questions=total_questions,
                         average_score=round(average_score, 1),
                         highest_score=round(highest_score, 1),
                         subject_chart_config=subject_chart_config,
                         month_chart_config=month_chart_config)

@user.route('/search', methods=['GET', 'POST'])
@user_required
def search():
    form = UserSearchForm()
    results = []
    
    if form.validate_on_submit():
        search_query = form.search_query.data
        search_type = form.search_type.data
        
        if search_type == 'subjects':
            results = Subject.query.filter(
                Subject.name.ilike(f'%{search_query}%')
            ).all()
        elif search_type == 'quizzes':
            results = Quiz.query.filter(
                or_(
                    Quiz.title.ilike(f'%{search_query}%'),
                    Quiz.description.ilike(f'%{search_query}%')
                )
            ).join(Chapter).join(Subject).filter(
                Subject.is_active == True
            ).all()
    
    return render_template('user/search.html', form=form, results=results) 

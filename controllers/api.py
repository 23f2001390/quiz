from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.quiz import Subject, Chapter, Quiz
from models.score import Score
from models.user import User
from quiz_utils import QuizTimer

api = Blueprint('api', __name__, url_prefix='/api')

# Helper function to serialize objects
def serialize_subject(subject):
    return {
        'id': subject.id,
        'name': subject.name,
        'description': subject.description,
        'chapters_count': len(subject.chapters)
    }

def serialize_chapter(chapter):
    return {
        'id': chapter.id,
        'name': chapter.name,
        'description': chapter.description,
        'subject_id': chapter.subject_id,
        'subject_name': chapter.subject.name,
        'quizzes_count': len(chapter.quizzes)
    }

def serialize_quiz(quiz):
    return {
        'id': quiz.id,
        'title': quiz.title,
        'description': quiz.description,
        'chapter_id': quiz.chapter_id,
        'chapter_name': quiz.chapter.name,
        'subject_name': quiz.chapter.subject.name,
        'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M'),
        'duration_minutes': quiz.duration_minutes,
        'questions_count': len(quiz.questions)
    }

def serialize_score(score):
    return {
        'id': score.id,
        'user_id': score.user_id,
        'quiz_id': score.quiz_id,
        'quiz_title': score.quiz.title,
        'score': score.score,
        'total_questions': score.total_questions,
        'percentage': round((score.score / score.total_questions * 100), 2) if score.total_questions > 0 else 0,
        'time_taken': score.time_taken,
        'attempted_at': score.attempted_at.strftime('%Y-%m-%d %H:%M')
    }

# Subject endpoints
@api.route('/subjects')
@login_required
def get_subjects():
    subjects = Subject.query.all()
    return jsonify({
        'success': True,
        'subjects': [serialize_subject(subject) for subject in subjects]
    })

@api.route('/subjects/<int:id>')
@login_required
def get_subject(id):
    subject = Subject.query.get_or_404(id)
    return jsonify({
        'success': True,
        'subject': serialize_subject(subject)
    })

# Chapter endpoints
@api.route('/subjects/<int:subject_id>/chapters')
@login_required
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify({
        'success': True,
        'chapters': [serialize_chapter(chapter) for chapter in chapters]
    })

@api.route('/chapters/<int:id>')
@login_required
def get_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    return jsonify({
        'success': True,
        'chapter': serialize_chapter(chapter)
    })

# Quiz endpoints
@api.route('/chapters/<int:chapter_id>/quizzes')
@login_required
def get_quizzes(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return jsonify({
        'success': True,
        'quizzes': [serialize_quiz(quiz) for quiz in quizzes]
    })

@api.route('/quizzes/<int:id>')
@login_required
def get_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    return jsonify({
        'success': True,
        'quiz': serialize_quiz(quiz)
    })

# Score endpoints
@api.route('/scores')
@login_required
def get_scores():
    if current_user.is_admin:
        # Admin can see all scores
        scores = Score.query.all()
    else:
        # Users can only see their own scores
        scores = Score.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'success': True,
        'scores': [serialize_score(score) for score in scores]
    })

@api.route('/users/<int:user_id>/scores')
@login_required
def get_user_scores(user_id):
    if not current_user.is_admin and current_user.id != user_id:
        return jsonify({
            'success': False,
            'message': 'Access denied'
        }), 403
    
    scores = Score.query.filter_by(user_id=user_id).all()
    return jsonify({
        'success': True,
        'scores': [serialize_score(score) for score in scores]
    })

@api.route('/quizzes/<int:quiz_id>/scores')
@login_required
def get_quiz_scores(quiz_id):
    if current_user.is_admin:
        # Admin can see all scores for a quiz
        scores = Score.query.filter_by(quiz_id=quiz_id).all()
    else:
        # Users can only see their own score for a quiz
        scores = Score.query.filter_by(quiz_id=quiz_id, user_id=current_user.id).all()
    
    return jsonify({
        'success': True,
        'scores': [serialize_score(score) for score in scores]
    })

@api.route('/current_time')
@login_required
def get_current_time():
    quiz_id = request.args.get('quiz_id', type=int)
    if not quiz_id:
        return jsonify({
            'success': False,
            'message': 'Quiz ID is required'
        }), 400
    
    seconds_remaining = QuizTimer.get_remaining_time(quiz_id)
    return jsonify({
        'success': True,
        'seconds_remaining': seconds_remaining
    })

# Error handlers
@api.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404

@api.errorhandler(403)
def forbidden_error(error):
    return jsonify({
        'success': False,
        'message': 'Access denied'
    }), 403 
from datetime import datetime, timedelta
from flask import session

class QuizTimer:
    @staticmethod
    def start_quiz(quiz_id, duration_minutes):
        """Initialize quiz timer"""
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        session[f'quiz_{quiz_id}_start'] = start_time.timestamp()
        session[f'quiz_{quiz_id}_end'] = end_time.timestamp()
        
        return start_time, end_time
    
    @staticmethod
    def get_remaining_time(quiz_id):
        """Get remaining time in seconds"""
        if f'quiz_{quiz_id}_end' not in session:
            return 0
            
        end_time = datetime.fromtimestamp(session[f'quiz_{quiz_id}_end'])
        remaining = (end_time - datetime.now()).total_seconds()
        
        return max(0, int(remaining))
    
    @staticmethod
    def get_time_taken(quiz_id):
        """Calculate time taken in seconds"""
        if f'quiz_{quiz_id}_start' not in session:
            return 0
            
        start_time = datetime.fromtimestamp(session[f'quiz_{quiz_id}_start'])
        time_taken = (datetime.now() - start_time).total_seconds()
        
        return int(time_taken)
    
    @staticmethod
    def is_time_up(quiz_id):
        """Check if quiz time is up"""
        remaining = QuizTimer.get_remaining_time(quiz_id)
        return remaining <= 0
    
    @staticmethod
    def clear_timer(quiz_id):
        """Clear timer data from session"""
        session.pop(f'quiz_{quiz_id}_start', None)
        session.pop(f'quiz_{quiz_id}_end', None)

def format_time(seconds):
    """Format seconds into MM:SS"""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}" 
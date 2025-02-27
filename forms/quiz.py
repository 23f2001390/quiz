from flask_wtf import FlaskForm
from wtforms import RadioField, HiddenField, SubmitField
from wtforms.validators import DataRequired

class QuizAttemptForm(FlaskForm):
    time_taken = HiddenField('Time Taken', validators=[DataRequired()])
    submit = SubmitField('Submit Quiz')
    
    def __init__(self, *args, **kwargs):
        super(QuizAttemptForm, self).__init__(*args, **kwargs)
        # Dynamic fields will be added in the view function

    @staticmethod
    def question_field():
        return RadioField('Answer', 
                        choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')],
                        coerce=int,
                        validators=[DataRequired()]) 
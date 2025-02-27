from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length, NumberRange

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class QuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    date_of_quiz = DateTimeLocalField('Date and Time of Quiz', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    duration_hours = IntegerField('Hours', validators=[NumberRange(min=0, max=3)], default=0)
    duration_minutes = IntegerField('Minutes', validators=[NumberRange(min=0, max=59)], default=30)
    submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
    question_text = TextAreaField('Question', validators=[DataRequired()])
    option_1 = StringField('Option 1', validators=[DataRequired(), Length(max=200)])
    option_2 = StringField('Option 2', validators=[DataRequired(), Length(max=200)])
    option_3 = StringField('Option 3', validators=[DataRequired(), Length(max=200)])
    option_4 = StringField('Option 4', validators=[DataRequired(), Length(max=200)])
    correct_option = SelectField('Correct Option', 
                               choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')],
                               coerce=int,
                               validators=[DataRequired()])
    submit = SubmitField('Submit')

class AdminSearchForm(FlaskForm):
    search_query = StringField('Search', validators=[DataRequired()])
    search_type = SelectField('Search In', 
                            choices=[('users', 'Users'), 
                                   ('subjects', 'Subjects'),
                                   ('quizzes', 'Quizzes'),
                                   ('questions', 'Questions')],
                            validators=[DataRequired()])
    submit = SubmitField('Search') 
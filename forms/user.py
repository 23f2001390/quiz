from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class UserSearchForm(FlaskForm):
    search_query = StringField('Search', validators=[DataRequired()])
    search_type = SelectField('Search In',
                            choices=[('subjects', 'Subjects'),
                                   ('quizzes', 'Quizzes')],
                            validators=[DataRequired()])
    submit = SubmitField('Search') 
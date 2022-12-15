from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired


# Create task form
class TodoForm(FlaskForm):
    task_name = StringField('Name', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('High priority', 'High priority'), ('Medium priority', 'Medium priority'), ('Low priority', 'Low priority')])
    status = IntegerField('Status', validators=[DataRequired()])
    submit = SubmitField('Create')

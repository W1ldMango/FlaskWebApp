from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


# Create task form for edit tasks
class EditTaskForm(FlaskForm):
    task_name = StringField('Name', validators=[DataRequired()])
    priority = SelectField('Priority',
                           choices=[('High priority', 'High priority'), ('Medium priority', 'Medium priority'),
                                    ('Low priority', 'Low priority')])
    submit = SubmitField('Accept')

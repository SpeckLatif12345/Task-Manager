from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError
from App.models import Task


class NewTaskForm(FlaskForm):
    task_name = StringField("Task Name", validators=[DataRequired()])

    task_description = TextAreaField("Task Description", validators=[DataRequired()])

    start_date = DateField("Start Date", format="%Y-%m-%d", validators=[DataRequired()])
    end_date = DateField("End Date", format="%Y-%m-%d", validators=[DataRequired()])

    submit = SubmitField("Save Task")

    def check_task_exist(self, task_name):
        task = Task.query.filter_by(task_name=task_name).first()
        if task is not None:
            raise ValidationError("Please use a different name ")
        return True

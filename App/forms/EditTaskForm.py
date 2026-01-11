from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


class EditTaskForm(FlaskForm):
    task_name = StringField("Task Name", validators=[DataRequired()])

    task_description = TextAreaField("Task Description", validators=[DataRequired()])

    task_date = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])

    task_status = SelectField(
        "Status",
        choices=[
            ("pending", "Pending"),
            ("active", "Active"),
            ("completed", "Completed"),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField("Update Task")

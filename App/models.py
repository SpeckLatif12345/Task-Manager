from datetime import date
from sqlalchemy import String, Date, false
from sqlalchemy.orm import Mapped, mapped_column
from wtforms.validators import ValidationError
from sql_alchemy_initialize import db


class Task(db.Model):
    __table_args__ = {"extend_existing": True}
    task_id: Mapped[str] = mapped_column(primary_key=True)
    task_name: Mapped[str] = mapped_column(
        String(100), index=True, unique=True, nullable=False
    )
    task_description: Mapped[str] = mapped_column(nullable=True)
    start_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    # This is a custom field validator used in WTForms Flask forms
    # WTForms automatically looks for functions named: validate_<field_name>
    #  So if your form has a field called: end_date = DateField(...)
    #  WTForms will automatically call: validate_end_date(...) during form validation.
    def validate_end_date(self, field):
        if field.data < self.start_date.data:
            raise ValidationError("End date must be after start date")

    # checking if task exist
    def validate_task_name(self, field):
        existing_task = Task.query.filter_by(task_name=field.data).first()
        if existing_task:
            raise ValidationError("Task name already exists")

    # for updating status
    def update_status(self):
        today = date.today()
        if today < self.start_date:
            self.status = "upcoming"
        elif self.start_date <= today <= self.end_date:
            self.status = "in_progress"
        else:
            self.status = "completed"

    # total days
    def total_days(self):
        total_days = (self.end_date - self.start_date).days
        return max(total_days, 0)

    # remaining days
    def remaining_days(self):
        today = date.today()
        return max(
            (self.end_date - today).days, 0
        )  # returns days left only as int and  should be greater than 0 else return 0

    # progress percentage
    def progress_percentage(self):
        today = date.today()
        total_days = (
            self.end_date - self.start_date
        ).days  # getting number of days from start to end(total)
        days_left = max((self.end_date - today).days, 0)  # getting number of days left

        # setting  a return limit - between 0 and 100
        if today <= self.start_date:
            return 0
        elif today >= self.end_date:
            return 100
        else:
            days_completed = total_days - days_left  # getting days completed
            progress = (days_completed / total_days) * 100
            return min(
                round(progress), 100
            )  # round to the nearest whole number  and return the smallest number ,(progress or 100)

from flask import render_template, request, flash, redirect, url_for, session, abort
from App import app
from App import db
from models import Task
from forms.new_task import NewTaskForm
from nanoid import generate
from datetime import date


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/taskManager/home")
def home():
    delete_form = NewTaskForm()
    tasks = Task.query.order_by(Task.start_date).all()

    # Auto-update status
    for task in tasks:
        task.update_status()
    db.session.commit()  # Save updated statuses

    return render_template("home.html", tasks=tasks, delete_form=delete_form)


@app.route("/taskManager/new_task", methods=["GET", "POST"])
def new_task():
    form = NewTaskForm()

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        today = date.today()

        if start_date <= today:
            status = "upcoming"
        elif start_date > today <= end_date:
            status = "in_progress"
        else:
            status = "completed"

        task = Task(
            task_id=generate(size=10),
            task_name=form.task_name.data,
            task_description=form.task_description.data,
            start_date=start_date,
            end_date=end_date,
            status=status,
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created successfully!", "success")

        return redirect(url_for("new_task"))

    return render_template("new_task.html", form=form)


@app.route("/taskManager/progress")
def progress():

    tasks = Task.query.order_by(Task.start_date).all()

    # Auto-update status
    for task in tasks:
        task.update_status()
    db.session.commit()  # Save updated statuses
    return render_template("progress.html", tasks=tasks)


@app.route("/taskManager/edit_task<string:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = NewTaskForm(obj=task)  # pre-fill form

    if form.validate_on_submit():
        task.task_name = form.task_name.data
        task.task_description = form.task_description.data
        task.start_date = form.start_date.data
        task.end_date = form.end_date.data

        db.session.commit()
        flash("Task Updated Successfully")

    return render_template("edit_task.html", form=form, task=task)


@app.route("/taskManager/delete_task<string:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.filter_by(task_id=task_id).first()  # get id of task

    if not task:
        abort(404)  # stops  and sends 404 page if task not found

    db.session.delete(task)  # delete task
    db.session.commit()  # save

    flash("Task deleted successfully", "success")

    return redirect(url_for("home"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

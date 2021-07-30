from flask import Flask,render_template,g,request,flash,Blueprint,url_for,redirect
from datetime import datetime
from werkzeug.exceptions import abort

tk = Blueprint("task","task")

from . import db
from . import auth

def get_task_details(task_id):
    user_id = g.user[0]
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("select * from task_list where t_id=%s",(task_id,))
    task = cur.fetchone()
    if task is None:
        abort(404, f"Task id {task_id} doesn't exist.")

    if task[1] != user_id:
        abort(403)

    return task

@tk.route('/')
@auth.login_required
def index():
    user_id = g.user[0]
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("select * from task_list where auth_id = %s order by created",(user_id,))
    all_task = cur.fetchall()
    return render_template("/task/index.html",tasks = all_task)

@tk.route("/create" , methods=["GET", "POST",])
@auth.login_required
def create():
    if request.method == "POST":
        task_title = request.form["title"]
        task_description = request.form["body"]
        schedule = request.form["schedule"]
        error = None

        if not task_title:
            error = "Task title is required"
        if error is None:
            user_id = g.user[0]
            conn = db.get_db()
            cur = conn.cursor()
            time_now = str(datetime.now())
    
            cur.execute("insert into task_list (auth_id,title,description,schedule,created,status) values (%s,%s,%s,%s,%s,%s) ", (user_id, task_title, task_description, schedule, time_now[:-7], 2))
            conn.commit()
            return redirect(url_for("task.index"))
        else:
            flash(error)
        
    return render_template("/task/create.html")

@tk.route("/<int:task_id>/update", methods=["GET", "POST"])
@auth.login_required
def update(task_id):
    task = get_task_details(task_id)
    if request.method == "POST":
        task_title = request.form["title"]
        task_description = request.form["body"]
        schedule = request.form["schedule"]
        print(schedule)
        error = None

        if not task_title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            user_id = g.user[0]
            conn = db.get_db()
            cur = conn.cursor()
            time_now = str( datetime.now() )

            cur.execute("update task_list set title = %s, description = %s, schedule = %s, updated = %s where t_id = %s",(task_title,task_description,schedule,time_now[:-7],task_id))
            
            conn.commit()
            return redirect(url_for("task.index"))
    return render_template("/task/update.html", task = task)

@tk.route("/<int:task_id>/delete", methods=["POST","GET"])
@auth.login_required
def delete(task_id):
    task = get_task_details(task_id)
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("delete from task_list where t_id=%s", (task_id,))
    conn.commit()
    return redirect(url_for("task.index"))
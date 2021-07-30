from datetime import datetime
import  functools

from flask import Flask, render_template, request, url_for, Blueprint, g, flash, redirect, session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', 'auth', url_prefix='/auth')

from . import db

def login_required(view):
    
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("select * from todo_user where u_id = %s", (user_id,))
        g.user = cur.fetchone()

@bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repass']
        error= None
        conn = db.get_db()
        cur = conn.cursor()

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif not repassword:
            error = "Re-enter the password"
        elif password != repassword:
            error = "Please enter same password in both fields."
        if error is None:
            # This checks whether the user exist already.
            cur.execute("select u_id from todo_user where u_name =%s",(username,))
            user = cur.fetchone()
            if user is not None:
                error = f"{username} already exists!"
        
        time_now = datetime.now()
        if error is None:
            cur.execute("insert into todo_user (u_name,pass,created) values (%s,%s,%s)", (username, generate_password_hash(password, method="sha256"),time_now))
            conn.commit()
            conn.close()
            return redirect(url_for("auth.login"))
        
        flash(error, category="'error'")

    return render_template("/auth/register.html")
    

@bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        message = None

        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("select * from todo_user where u_name = %s", (username,))
        user = cur.fetchone()
        if user is None:
            message = "Invalid username"
        elif not check_password_hash(user[2], password):
            message = "Incorrect password"

        if message is None:
            session.clear()
            session["user_id"] = user[0]
            return redirect(url_for("task.index"))

        flash(message, category="'error'")

    return render_template("/auth/login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("task.index"))
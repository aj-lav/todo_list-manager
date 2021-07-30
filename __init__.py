from flask import Flask, render_template,request

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
    DATABASE="todo",
    SECRET_KEY = "This is the secret key"
    )

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import task
    app.register_blueprint(task.tk)
    app.add_url_rule("/", endpoint="index")
    return app
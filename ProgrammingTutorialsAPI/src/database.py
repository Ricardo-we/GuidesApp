from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def db_init(app):
    global db
    db.init_app(app)
    db.create_all()
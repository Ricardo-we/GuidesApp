from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
marsh = Marshmallow()
        
class Guides(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guide_section = db.Column(db.String(70))
    guide_name = db.Column(db.String(70))
    guide_body = db.Column(db.Text)
    guide_close = db.Column(db.Text)
    def __init__(self, guide_section, guide_name, guide_body, guide_close):
        self.guide_section = guide_section
        self.guide_name = guide_name
        self.guide_body = guide_body
        self.guide_close = guide_close

class GuidesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Guides

class GuidesImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guide_name = db.Column(db.String(70))
    guide_image_1 = db.Column(db.LargeBinary, nullable=False)
    guide_image_2 = db.Column(db.LargeBinary)
    def __init__(self, guide_name, guide_image_1, guide_image_2):
        self.guide_name = guide_name
        self.guide_image_1 = guide_image_1
        self.guide_image_2 = guide_image_2

class GuidesImagesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = GuidesImages

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90))
    password = db.Column(db.String(90))
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = User
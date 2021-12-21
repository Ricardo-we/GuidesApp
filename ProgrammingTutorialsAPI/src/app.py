from os import error
from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow
from models import *        
from io import BytesIO
from pprint import pprint

# APP CONFIG AND DATABASE
DB_URL = 'mysql://root:@localhost:3306/guides'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
marsh.init_app(app)
#  SCHEMAS
guide_schema = GuidesSchema()
guides_schema = GuidesSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# ROUTES
CORS(app, resources={r'/guides/*': {'origins': 'http://localhost:3000'}, r'/users/*': {'origins': 'http://localhost:3000'}})
@app.route('/guides', methods=['POST'])
def add_guide():
    try:
        guide_section = request.json['guide_section']
        guide_name =  request.json['guide_name']
        guide_content = request.json['guide_content']
        guide_close = request.json['guide_close']
        new_guide = Guides(guide_section, guide_name, guide_content, guide_close)
        
        db.session.add(new_guide)
        
        # guide_image_1 = request.json['guide_image_1']
        # guide_image_2 = request.json['guide_image_2']   
        # new_guide_images = GuidesImages(guide_name, guide_image_1, guide_image_2)
        # db.session.add(new_guide_images)
        
        db.session.commit()
        return "received"
    except: 
        return "Something failed"

@app.route('/guides', methods=['GET'])
def get_guides():
    try:
        all_guides = Guides.query.all()
        return jsonify(guides_schema.dump(all_guides))
    except: 
        return "Something failed"
        
@app.route('/guides/<id>', methods=['GET'])
def get_guide(id):
    try:
        requested_guides = Guides.query.get(id)
        return guide_schema.dump(requested_guides)
    except:
        return 'Something failed'

@app.route('/guides/<id>', methods=['DELETE'])
def delete_guide(id):
    try:
        guide = Guides.query.get(id)
        db.session.delete(guide)
        db.session.commit()
        return 'Deleted successfully'
    except: 
        return 'Something failed'

@app.route('/guides/<id>', methods=['PUT'])
def update_guide(id):
    try:
        guide = Guides.query.get(id)
        guide.guide_section = request.json['guide_section']
        guide.guide_name =  request.json['guide_name']
        guide.guide_content = request.json['guide_content']
        guide.guide_close = request.json['guide_close']
    
        guide_images = GuidesImages.query.get(id)
        guide_images.guide_image_1 = request.files['guide_image_1']
        guide_images.guide_image_2 = request.files['guide_image_2']   
        return "Updated successfully"
    except:
        return 'Something failed'

@app.route('/users/<user>', methods=['POST', 'GET', 'DELETE', 'PUT'])
def user_access(user):
    if request.method == 'POST':
        try:
            username = request.json['username']
            password = request.json['password']
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return 'username'
        except:
            return 'Something failed'
    elif request.method == 'GET':
        try:
            username = request.args.get('username')
            password = request.args.get('password')
            print("username: ", username)
            print("password: ", password)
            finaluser = User.query.filter_by(username=username,password=password).first()
            return jsonify(user_schema.dump(finaluser))
        except:
            return 'Something failed'
    elif request.method == 'DELETE':
        try:
            deleted_user = User.query.filter_by(id=user)
            db.session.delete(deleted_user)
            db.session.commit()
            return 'Deleted successfully'
        except:
            return 'Something failed'
    elif request.method == 'PUT':
        try:
            updated_user = User.query.filter_by(id=user)
            updated_user.username = request.json['username']
            updated_user.password = request.json['password']
            return 'Updated successfully'
        except:
            return 'Something failed'
    else:
        return 'Method not allowed'
@app.route('/users/', methods=['GET'])
def get_users():
    all_users = User.query.all()
    return jsonify(users_schema.dump(all_users))

if __name__ == '__main__':
    app.run(debug=True)
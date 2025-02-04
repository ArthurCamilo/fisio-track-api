from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from app import db
from app.models import User
from app.routes import bp

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201
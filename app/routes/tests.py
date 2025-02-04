import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import Test
from app.routes import bp

@bp.route('/tests', methods=['POST'])
@jwt_required()
def create_test():
    data = request.get_json()
    new_test = Test(
        date=datetime.datetime.strptime(data['date'], '%Y-%m-%d').date(),
        patient_id=data['patient_id'],
        test_setup_id=data['test_setup_id'],
        is_completed=data.get('is_completed', False)
    )
    db.session.add(new_test)
    db.session.commit()
    return jsonify({"msg": "Test created"}), 201

@bp.route('/tests', methods=['GET'])
@jwt_required()
def get_all_tests():
    tests = Test.query.filter_by(is_active=True).all()
    tests_list = []
    for test in tests:
        tests_list.append({
            "id": test.id,
            "date": test.date.isoformat(),
            "patient_id": test.patient_id,
            "test_setup_id": test.test_setup_id,
            "is_active": test.is_active,
            "is_completed": test.is_completed
        })
    return jsonify(tests_list), 200

@bp.route('/tests/<int:test_id>', methods=['GET'])
@jwt_required()
def get_test(test_id):
    test = Test.query.filter_by(id=test_id, is_active=True).first()
    if not test:
        return jsonify({"msg": "Test not found"}), 404
    return jsonify({
        "id": test.id,
        "date": test.date.isoformat(),
        "patient_id": test.patient_id,
        "test_setup_id": test.test_setup_id,
        "is_active": test.is_active,
        "is_completed": test.is_completed
    }), 200

@bp.route('/tests/<int:test_id>', methods=['PUT'])
@jwt_required()
def edit_test(test_id):
    data = request.get_json()
    test = Test.query.filter_by(id=test_id, is_active=True).first()
    if not test:
        return jsonify({"msg": "Test not found"}), 404

    test.date = datetime.datetime.strptime(data.get('date'), '%Y-%m-%d').date() if 'date' in data else test.date
    test.patient_id = data.get('patient_id', test.patient_id)
    test.test_setup_id = data.get('test_setup_id', test.test_setup_id)
    test.is_completed = data.get('is_completed', test.is_completed)

    db.session.commit()
    return jsonify({"msg": "Test updated"}), 200

@bp.route('/tests/<int:test_id>', methods=['DELETE'])
@jwt_required()
def delete_test(test_id):
    test = Test.query.filter_by(id=test_id, is_active=True).first()
    if not test:
        return jsonify({"msg": "Test not found"}), 404

    test.is_active = False
    db.session.commit()
    return jsonify({"msg": "Test inactivated"}), 200
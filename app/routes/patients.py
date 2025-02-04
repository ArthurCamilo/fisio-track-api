import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import Patient
from app.routes import bp

@bp.route('/patients', methods=['POST'])
@jwt_required()
def create_patient():
    data = request.get_json()
    new_patient = Patient(
        name=data['name'],
        date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d'),
        cpf_or_rg=data.get('cpf_or_rg'),
        gender=data['gender']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"msg": "Patient created"}), 201

@bp.route('/patients', methods=['GET'])
@jwt_required()
def get_all_patients():
    patients = Patient.query.filter_by(is_active=True).all()
    patients_list = []
    for patient in patients:
        patients_list.append({
            "id": patient.id,
            "name": patient.name,
            "date_of_birth": patient.date_of_birth.isoformat(),
            "cpf_or_rg": patient.cpf_or_rg,
            "gender": patient.gender,
            "is_active": patient.is_active
        })
    return jsonify(patients_list), 200

@bp.route('/patients/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    patient = Patient.query.filter_by(id=patient_id, is_active=True).first()
    if not patient:
        return jsonify({"msg": "Patient not found"}), 404
    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "date_of_birth": patient.date_of_birth.isoformat(),
        "cpf_or_rg": patient.cpf_or_rg,
        "gender": patient.gender,
        "is_active": patient.is_active
    }), 200

@bp.route('/patients/<int:patient_id>', methods=['PUT'])
@jwt_required()
def edit_patient(patient_id):
    data = request.get_json()
    patient = Patient.query.filter_by(id=patient_id, is_active=True).first()
    if not patient:
        return jsonify({"msg": "Patient not found"}), 404

    patient.name = data.get('name', patient.name)
    patient.date_of_birth = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d') if 'date_of_birth' in data else patient.date_of_birth
    patient.cpf_or_rg = data.get('cpf_or_rg', patient.cpf_or_rg)
    patient.gender = data.get('gender', patient.gender)

    db.session.commit()
    return jsonify({"msg": "Patient updated"}), 200

@bp.route('/patients/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    patient = Patient.query.filter_by(id=patient_id, is_active=True).first()
    if not patient:
        return jsonify({"msg": "Patient not found"}), 404

    patient.is_active = False
    db.session.commit()
    return jsonify({"msg": "Patient inactivated"}), 200
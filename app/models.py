from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    cpf_or_rg = db.Column(db.String(20))
    gender = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    test_setup_id = db.Column(db.Integer, db.ForeignKey('test_setup.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_completed = db.Column(db.Boolean, default=True, nullable=False)

class TestRepetition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    repetition = db.Column(db.Integer, nullable=False)
    weight_variation = db.Column(db.JSON, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class TestSetup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    effort_duration = db.Column(db.Integer, nullable=False)
    rest_duration = db.Column(db.Integer, nullable=False)
    repetitions = db.Column(db.Integer, nullable=False)
    muscle_group = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

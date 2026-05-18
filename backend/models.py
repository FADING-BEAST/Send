from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='Staff')  # Admin or Staff
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return str(self.id)

    @property
    def active(self):
        return self.is_active

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer) # 100, 200, etc
    enrollment_year = db.Column(db.Integer)
    progression_status = db.Column(db.String(50), default='Good Standing')
    notes = db.Column(db.Text, default='')

    records = db.relationship('AcademicRecord', backref='student', lazy='dynamic')
    analysis = db.relationship('RiskAnalysis', backref='student', uselist=False)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    credit_units = db.Column(db.Integer, default=3)
    is_core = db.Column(db.Boolean, default=False)

class AcademicRecord(db.Model):
    __tablename__ = 'academic_records'
    id = db.Column(db.Integer, primary_key=True)
    student_db_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    grade = db.Column(db.String(2))
    score = db.Column(db.Float)
    semester = db.Column(db.Integer) # 1 or 2
    session = db.Column(db.String(20)) # e.g. 2023/2024
    attempt_number = db.Column(db.Integer, default=1)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

class RiskAnalysis(db.Model):
    __tablename__ = 'risk_analysis'
    id = db.Column(db.Integer, primary_key=True)
    student_db_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    risk_score = db.Column(db.Float)
    risk_category = db.Column(db.String(20)) # High, Medium, Low
    factors = db.Column(db.Text) # JSON string of contributing factors
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class RiskRule(db.Model):
    __tablename__ = 'risk_rules'
    id = db.Column(db.Integer, primary_key=True)
    rule_key = db.Column(db.String(50), unique=True) # e.g. 'gpa_high_threshold'
    value = db.Column(db.Float)
    description = db.Column(db.String(255))

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ImportLog(db.Model):
    __tablename__ = 'import_logs'
    id = db.Column(db.Integer, primary_key=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    records_added = db.Column(db.Integer, default=0)
    duplicates_skipped = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='Success')  # Success / Failed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    uploader = db.relationship('User', backref='imports', foreign_keys=[uploaded_by])

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    category = db.Column(db.String(20), default='info')  # info | warning | danger
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='notifications', foreign_keys=[user_id])

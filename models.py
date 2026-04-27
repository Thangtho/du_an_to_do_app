# ============================================================
# models.py
# Tách User và Task ra file riêng để tránh circular import
# giữa auth.py và tasks.py
# ============================================================

from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('Task', backref='owner', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        from app import bcrypt
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        from app import bcrypt
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id':         self.id,
            'username':   self.username,
            'email':      self.email,
            'created_at': self.created_at.isoformat()
        }


class Task(db.Model):
    __tablename__ = 'tasks'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    status      = db.Column(db.String(20),  default='todo')
    priority    = db.Column(db.String(10),  default='medium')
    deadline    = db.Column(db.DateTime, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def is_overdue(self):
        if self.deadline and self.status != 'done':
            return datetime.utcnow() > self.deadline
        return False

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'description': self.description,
            'status':      self.status,
            'priority':    self.priority,
            'deadline':    self.deadline.isoformat() if self.deadline else None,
            'created_at':  self.created_at.isoformat(),
            'updated_at':  self.updated_at.isoformat() if self.updated_at else None,
            'is_overdue':  self.is_overdue(),
            'user_id':     self.user_id
        }

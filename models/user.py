# -*- coding: utf-8 -*-

# python imports
from datetime import datetime

# project import :
from flask import session

# project imports :
from controller.extension import db

__author__ = 'Amir Mohammad'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    passwordhash = db.Column(db.String(64), nullable=False)
    firstname = db.Column(db.Unicode(254))
    lastname = db.Column(db.Unicode(254))
    gender = db.Column(db.Enum('Male', 'Female', name='gender'), default='Male', nullable=True)
    phones = db.Column(db.BigInteger, nullable=False)
    brand = db.Column(db.Unicode(254), nullable=False)
    category = db.Column(db.Unicode(254), nullable=False)

    logs = db.relationship("Log", lazy='dynamic', backref='user')

    def to_json(self, with_logs=False):
        if with_logs:
            _dict = self.to_json()
            _dict['logs'] = [log.to_json() for log in self.logs]
            return _dict
        return {
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'gender': self.gender,
            'phones': self.phones,
            'brand': self.brand,
            'category': self.category,
        }

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.username)

    def login(self):
        session['username'] = self.username

    @staticmethod
    def logout():
        session.pop('username', None)

    @staticmethod
    def logged_in_user():
        return session.get('username', None)

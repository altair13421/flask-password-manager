from app import app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    passwords = db.relationship('Passwords', backref='user', lazy='dynamic')

    @login.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    def set_password(self, passwordtoset):
        self.password = generate_password_hash(passwordtoset)
    
    def check_password(self, passwordtocheck):
        return check_password_hash(self.password, passwordtocheck)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'<Saved Password {self.username} {self.url} USER {self.userid}>'
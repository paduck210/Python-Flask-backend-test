from alayatodo import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    completed = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Todo {}>'.format(self.description)

    def mark_completed(self):
        self.completed = 1

    def mark_uncompleted(self):
        self.completed = 0

    def make_dict(self):
        return {
            "id" : self.id,
            "description" : self.description,
            "user_id" : self.user_id,
            "completed" : self.completed
        }
from app import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    date_to_do = db.Column(db.Date(), nullable=False)
    mark = db.Column(db.Boolean(), default=False)

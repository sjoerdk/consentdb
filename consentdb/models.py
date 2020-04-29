from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ConsentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mdn = db.Column(db.String(80), unique=True, nullable=False)
    can_use = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"{self.mdn}, can use:{self.can_use}"

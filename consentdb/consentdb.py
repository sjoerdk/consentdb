# -*- coding: utf-8 -*-

"""Main module."""
from consentdb import db, app


class ConsentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mdn = db.Column(db.String(80), unique=True, nullable=False)
    can_use = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"{self.mdn}, can use:{self.can_use}"


@app.route('/opt-out-test')
def test():
    return "yo momma man"


@app.route('/opt-out/')
def get_status_by_query_string():
    pid = request.args.get('pid')
    if not pid:
        return "missing parameter 'pid'", 400
    record = ConsentRecord.query.filter_by(mdn='z12345').first()
    if not record:
        return "Not found"
    if record.can_use:
        return "Not found"
    else:
        return "Objection"


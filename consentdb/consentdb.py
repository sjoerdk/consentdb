# -*- coding: utf-8 -*-

"""Main module."""
from consentdb import create_app
from consentdb.models import ConsentRecord

app = create_app()


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


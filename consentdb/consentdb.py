# -*- coding: utf-8 -*-

"""Main module."""
from flask import request
from flask.blueprints import Blueprint
from consentdb.models import ConsentRecord

# Blueprint instead of direct app() for easier testing
recipes_blueprint = Blueprint('recipes', __name__)

@recipes_blueprint.route('/opt-out-test')
def test():
    return "yo momma man"


@recipes_blueprint.route('/opt-out/')
def get_status_by_query_string():
    pid = request.args.get('pid')
    if not pid:
        return "missing parameter 'pid'", 400
    record = ConsentRecord.query.filter_by(mdn=pid).first()
    if not record:
        return "Not found"
    if record.can_use:
        return "Not found"
    else:
        return "Objection"


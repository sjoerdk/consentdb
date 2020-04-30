from flask import request
from flask.blueprints import Blueprint
from flask.helpers import url_for

from consentdb.models import ConsentRecord

# Blueprint instead of direct app() for easier testing
consentdb_blueprint = Blueprint('consentdb', __name__)


@consentdb_blueprint.route('/')
def index():
    return "consent db API"


@consentdb_blueprint.route('/opt-outs/', strict_slashes=False)
def opt_out():
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


@consentdb_blueprint.route('/opt-out-info')
def opt_out_info():
    return f"V1 API (opt-out), use {url_for('consentdb.opt_out', mdn='z1234567')}."


@consentdb_blueprint.route('/consent/')
def consent_info():
    return f"Missing patient ID. Please use" \
           f" {url_for('consentdb.consent', pid='<z1234567>')}.", 400


@consentdb_blueprint.route('/consent/<string:pid>')
def consent(pid):
    record = ConsentRecord.query.filter_by(mdn=pid).first()
    if not record:
        return 'record_not_found', 400
    if record.can_use:
        return "consent"
    else:
        return "no_consent"

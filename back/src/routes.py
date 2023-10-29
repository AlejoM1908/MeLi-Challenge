from flask import Blueprint

bp = Blueprint('main_v1', __name__, url_prefix='/v1.1')

@bp.route('/login/', methods=['GET'])
def login():
    # ToDo: Implement login
    pass

@bp.route('/logout/', methods=['GET'])
def logout():
    # ToDo: Implement logout
    pass

@bp.route('/refresh/', methods=['GET'])
def refresh():
    # ToDo: Implement refresh
    pass

@bp.route('/risks/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def risks():
    # Todo: Implement risks
    pass
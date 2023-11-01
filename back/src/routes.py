from flask import Blueprint, request, jsonify, current_app
from src.use_cases.AuthCases import *
from src.use_cases.ProvidersCases import *
from src.static.http_codes import HttpCodes
from functools import wraps

def secure_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'error': 'Missing token'}), HttpCodes.UNAUTHORIZED.value
        
        try:
            payload = verifyTokenUseCase(current_app.config['SECRETS']['jwt'], token)
        except Exception as e:
            return jsonify({'error': str(e)}), HttpCodes.UNAUTHORIZED.value
        
        if isinstance(payload, str):
            return jsonify({'error': 'Invalid token'}), HttpCodes.UNAUTHORIZED.value
        
        return f(payload['email'], *args, **kwargs)

    return decorated_function

bp = Blueprint('main_v1', __name__, url_prefix='/v1.1')

@bp.route('/login', methods=['GET'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
    
    if not 'email' in data or not 'password' in data:
        return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value

    login_result = loginUseCase(current_app.config['REPOSITORY'], data['email'], data['password'])
    if isinstance(login_result, str):
        return jsonify({'error': login_result}), HttpCodes.UNAUTHORIZED.value
    
    jwt_pair = generateJWTPairUseCase(current_app.config['SECRETS'], {'email': data['email']})
    if isinstance(jwt_pair, str):
        return jsonify({'error': jwt_pair}), HttpCodes.INTERNAL_SERVER_ERROR.value
    
    return jsonify({'jwt': jwt_pair[0], 'refresh': jwt_pair[1]}), HttpCodes.OK.value

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
    
    if not 'email' in data or not 'password' in data or not 'name' in data:
        return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
    
    register_result = registerUseCase(current_app.config['REPOSITORY'], data['email'], data['password'], data['name'])
    if isinstance(register_result, str):
        return jsonify({'error': register_result}), HttpCodes.CONFLICT.value
    
    return jsonify({'message': 'User registered'}), HttpCodes.CREATED.value

@bp.route('/refresh', methods=['GET'])
def refresh():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
    
    if not 'refresh' in data:
        return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
    
    jwt_pair = refreshUseCase(current_app.config['SECRETS'], data['refresh'])
    if isinstance(jwt_pair, str):
        return jsonify({'error': jwt_pair}), HttpCodes.UNAUTHORIZED.value
    
    return jsonify({'jwt': jwt_pair[0], 'refresh': jwt_pair[1]}), HttpCodes.OK.value

@bp.route('/providers', methods=['GET', 'POST'])
@secure_route
def providers(email):
    if request.method == 'GET':
        providers = getProvidersUseCase(current_app.config['REPOSITORY'])
        if isinstance(providers, str):
            return jsonify({'error': providers}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify([provider.asDict() for provider in providers]), HttpCodes.OK.value
    
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
        
        if not 'name' in data or not 'description' in data or not 'country' in data:
            return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
        
        operation = createProviderUseCase(current_app.config['REPOSITORY'], current_app.config['COUNTRY_API'], data['name'], data['description'], data['country'])
        if isinstance(operation, str):
            return jsonify({'error': operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify({'message': 'Provider created'}), HttpCodes.CREATED.value
    
@bp.route('/providers/<int:provider_id>', methods=['GET', 'PUT', 'DELETE'])
@secure_route
def query_provider(email, provider_id):
    if request.method == 'GET':
        provider = getProviderByIdUseCase(current_app.config['REPOSITORY'], provider_id)
        if isinstance(provider, str):
            return jsonify({'error': provider}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify(provider.asDict()), HttpCodes.OK.value
    
    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
        
        if not 'name' in data or not 'description' in data or not 'country' in data:
            return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
        
        operation = updateProviderUseCase(current_app.config['REPOSITORY'], current_app.config['COUNTRY_API'], provider_id, data['name'], data['description'], data['country'])
        if isinstance(operation, str):
            return jsonify({'error': operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify({'message': 'Provider updated'}), HttpCodes.OK.value
    
    if request.method == 'DELETE':
        operation = deleteProviderUseCase(current_app.config['REPOSITORY'], provider_id)
        if isinstance(operation, str):
            return jsonify({'error': operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify({'message': 'Provider deleted'}), HttpCodes.NO_CONTENT.value

@bp.route('/risks', methods=['GET', 'POST'])
@secure_route
def risks(email):
    if request.method == 'GET':
        risks = current_app.config['REPOSITORY'].getRisks()
        if isinstance(risks, str):
            return jsonify({'error': risks}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify([risk.serialize() for risk in risks]), HttpCodes.OK.value
    
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
        
        if not 'name' in data or not 'description' in data or not 'probability' in data or not 'impact' in data:
            return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
        
        operation = current_app.config['REPOSITORY'].createRisk(data['name'], data['description'], data['probability'], data['impact'])
        if isinstance(operation, str):
            return jsonify({'error': operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify({'message': 'Risk created'}), HttpCodes.CREATED.value

@bp.route('/risks/<int:risk_id>', methods=['GET', 'PUT', 'DELETE'])
@secure_route
def query_risk(email, risk_id):
    if request.method == 'GET':
        risk = current_app.config['REPOSITORY'].getRiskById(risk_id)
        if isinstance(risk, str):
            return jsonify({'error': risk}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify(risk.serialize()), HttpCodes.OK.value
    
    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
        
        if not 'name' in data or not 'description' in data or not 'probability' in data or not 'impact' in data:
            return jsonify({'error': 'Invalid request'}), HttpCodes.BAD_REQUEST.value
        
        operation = current_app.config['REPOSITORY'].updateRisk(risk_id, data['name'], data['description'], data['probability'], data['impact'])
        if isinstance(operation, str):
            return jsonify({'error': operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify({'message': 'Risk updated'}), HttpCodes.OK.value
    
    if request.method == 'DELETE':
        operation = current_app.config['REPOSITORY'].deleteRisk(risk_id)
        if isinstance(operation, str):
            return jsonify({'error': operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify({'message': 'Risk deleted'}), HttpCodes.OK.value
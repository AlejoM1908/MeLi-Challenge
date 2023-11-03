from flask import Blueprint, request, jsonify, current_app
from src.use_cases.AuthCases import loginUseCase, registerUseCase, refreshUseCase, verifyTokenUseCase, generateJWTPairUseCase
from src.use_cases.ProvidersCases import getProvidersUseCase, getProviderByIdUseCase, createProviderUseCase, updateProviderUseCase, deleteProviderUseCase, getProviderByNameUseCase
from src.use_cases.RisksCases import getFilteredRisksUseCase, createRiskUseCase, updateRiskUseCase, deleteRiskUseCase
from src.use_cases.UsersCases import getUserByEmailUseCase, getUserRolesUseCase, addRoleToUserUseCase, removeRoleFromUserUseCase, addUserToRiskUseCase, removeUserFromRiskUseCase
from src.use_cases.CountryCases import getCountryByCCA3UseCase
from src.use_cases.RolesCases import getRoleByIdUseCase, createRoleUseCase, updateRoleUseCase, deleteRoleUseCase, getRolesUseCase
from src.static.http_codes import HttpCodes

from src.entities.Country import Country
from src.entities.User import User
from src.entities.Provider import Provider
from src.entities.Risk import Risk

from functools import wraps

bp = Blueprint("main_v1", __name__, url_prefix="/v1.1")

def secure_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer ' not in auth_header:
            return jsonify({"error": "Missing token"}), HttpCodes.UNAUTHORIZED.value

        token = auth_header.split('Bearer ')[1]

        try:
            payload = verifyTokenUseCase(current_app.config["SECRETS"]["jwt"], token)
        except Exception as e:
            return jsonify({"error": str(e)}), HttpCodes.UNAUTHORIZED.value

        if isinstance(payload, str):
            return jsonify({"error": "Invalid token"}), HttpCodes.UNAUTHORIZED.value

        return f(payload["email"], *args, **kwargs)

    return decorated_function

def _extractFilters(filter_string: str) -> dict:
    if not filter_string:
        return {}
    else:
        filters = {}

    for filter in filter_string.split(","):
        # Check for a valid provider_id
        if filter.startswith("provider"):
            data = filter.split(":")[1]

            if not data.isdigit():
                query = getProviderByNameUseCase(current_app.config["REPOSITORY"], data)
                if isinstance(query, str):
                    return jsonify({"error": query}), HttpCodes.INTERNAL_SERVER_ERROR.value
                elif isinstance(query, list[Provider]):
                    data = query[0].id
                else:
                    return jsonify({"error": "The given provider does not exist"}), HttpCodes.NOT_FOUND.value

            filters["provider_id"] = int(data)

        # Check for a valid user_id
        elif filter.startswith("user"):
            data = filter.split(":")[1]

            if not data.isdigit():
                query = getUserByEmailUseCase(current_app.config["REPOSITORY"], data)
                if isinstance(query, str):
                    return jsonify({"error": query}), HttpCodes.INTERNAL_SERVER_ERROR.value
                elif isinstance(query, list[User]):
                    data = query[0].id
                else:
                    return jsonify({"error": "The given user does not exist"}), HttpCodes.NOT_FOUND.value

            filters["user_id"] = int(data)

        # Check for a valid probability
        elif filter.startswith("probability"):
            filters["probability"] = filter.split(":")[1]

        # Check for a valid impact
        elif filter.startswith("impact"):
            filters["impact"] = filter.split(":")[1]
        
        # Check for a valid country CCA3 or string
        elif len(filter) == 3:
            query = getCountryByCCA3UseCase(current_app.config["COUNTRY_API"], filter)
            if isinstance(query, Country):
                filters["country"] = query.cca3
            else:
                filters["string"] = filter

        # Add all the other filters to the string filter
        else:
            filters["string"] = filter

    return filters


@bp.route("/login", methods=["GET"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

    if not "email" in data or not "password" in data:
        return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

    login_result = loginUseCase(
        current_app.config["REPOSITORY"], data["email"], data["password"]
    )
    if isinstance(login_result, str):
        return jsonify({"error": login_result}), HttpCodes.UNAUTHORIZED.value

    jwt_pair = generateJWTPairUseCase(
        current_app.config["SECRETS"], {"email": data["email"]}
    )
    if isinstance(jwt_pair, str):
        return jsonify({"error": jwt_pair}), HttpCodes.INTERNAL_SERVER_ERROR.value

    return jsonify({"jwt": jwt_pair[0], "refresh": jwt_pair[1]}), HttpCodes.OK.value


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

    if not "email" in data or not "password" in data or not "name" in data:
        return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

    register_result = registerUseCase(
        current_app.config["REPOSITORY"], data["email"], data["password"], data["name"]
    )
    if isinstance(register_result, str):
        return jsonify({"error": register_result}), HttpCodes.CONFLICT.value

    return jsonify({"message": "User registered"}), HttpCodes.CREATED.value

@bp.route("/refresh", methods=["GET"])
def refresh():
    refresh_token = request.cookies.get('refresh_token')
    print(request.cookies)
    if not refresh_token:
        return jsonify({"error": "No refresh token provided"}), HttpCodes.BAD_REQUEST.value

    jwt_pair = refreshUseCase(current_app.config["SECRETS"], refresh_token)
    if isinstance(jwt_pair, str):
        return jsonify({"error": jwt_pair}), HttpCodes.UNAUTHORIZED.value

    return jsonify({"jwt": jwt_pair[0], "refresh": jwt_pair[1]}), HttpCodes.OK.value


@bp.route("/roles", methods=["GET", "POST"])
@secure_route
def roles(email):
    if request.method == "GET":
        roles = getRolesUseCase(current_app.config["REPOSITORY"])
        if isinstance(roles, str):
            return jsonify({"error": roles}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return (
            jsonify([role.asDict() for role in roles]),
            HttpCodes.OK.value,
        )
    
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        if not "name" in data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        operation = createRoleUseCase(
            current_app.config["REPOSITORY"],
            data["name"],
        )
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.BAD_REQUEST.value
        
        return jsonify({"message": "Role created", "id": operation}), HttpCodes.CREATED.value
    
@bp.route("/roles/<int:role_id>", methods=["GET", "PUT", "DELETE"])
@secure_route
def query_role(email, role_id):
    if request.method == "GET":
        role = getRoleByIdUseCase(current_app.config["REPOSITORY"], role_id)
        if isinstance(role, str):
            return jsonify({"error": role}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return jsonify(role.asDict()), HttpCodes.OK.value
    
    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        if not "name" in data and not "description" in data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        operation = updateRoleUseCase(
            current_app.config["REPOSITORY"],
            role_id,
            {key:value for key,value in data.items() if key in ["name", "description"]}
        )
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return jsonify({"message": "Role updated"}), HttpCodes.OK.value
    
    if request.method == "DELETE":
        operation = deleteRoleUseCase(current_app.config["REPOSITORY"], role_id)
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return jsonify({"message": "Role deleted"}), HttpCodes.OK.value

@bp.route("/providers", methods=["GET", "POST"])
@secure_route
def providers(email):
    if request.method == "GET":
        providers = getProvidersUseCase(current_app.config["REPOSITORY"])
        if isinstance(providers, str):
            return jsonify({"error": providers}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return (
            jsonify([provider.asDict() for provider in providers]),
            HttpCodes.OK.value,
        )

    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        if not "name" in data or not "description" in data or not "country" in data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        operation = createProviderUseCase(
            current_app.config["REPOSITORY"],
            current_app.config["COUNTRY_API"],
            data["name"],
            data["description"],
            data["country"],
        )
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify({"message": "Provider created", "id": operation}), HttpCodes.CREATED.value

@bp.route("/providers/<int:provider_id>", methods=["GET", "PUT", "DELETE"])
@secure_route
def query_provider(email, provider_id):
    if request.method == "GET":
        provider = getProviderByIdUseCase(current_app.config["REPOSITORY"], provider_id)
        if not isinstance(provider, Provider):
            return jsonify({"error": provider}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return jsonify(provider.asDict()), HttpCodes.OK.value

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        if not "name" in data and not "description" in data and not "country" in data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        operation = updateProviderUseCase(
            current_app.config["REPOSITORY"],
            current_app.config["COUNTRY_API"],
            provider_id,
            {key:value for key,value in data.items() if key in ["name", "description", "country"]}
        )
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return jsonify({"message": "Provider updated"}), HttpCodes.OK.value

    if request.method == "DELETE":
        operation = deleteProviderUseCase(current_app.config["REPOSITORY"], provider_id)
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return jsonify({"message": "Provider deleted"}), HttpCodes.OK.value


@bp.route("/risks", methods=["GET", "POST"])
@secure_route
def risks(email):
    if request.method == "GET":
        # Get the query parameters filter, divide it by comma and construct the filters dictionary
        filter_query = list(request.args.to_dict().keys())[0] if len(request.args.to_dict()) > 0 else None
        
        filters = _extractFilters(filter_query)

        risks = getFilteredRisksUseCase(current_app.config["REPOSITORY"], filters)
        if not isinstance(risks, list):
            return jsonify({"error": risks}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return (
            jsonify([risk.asDict() for risk in risks]),
            HttpCodes.OK.value,
        )
    
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        if (
            not "name" in data
            or not "description" in data
            or not "probability" in data
            or not "impact" in data
            or not "provider_id" in data
        ):
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        operation = createRiskUseCase(
            current_app.config["REPOSITORY"],
            data["provider_id"],
            data["name"],
            data["description"],
            data["probability"],
            data["impact"],
            email
        )
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return jsonify({"message": "Risk created"}), HttpCodes.CREATED.value


@bp.route("/risks/<int:risk_id>", methods=["GET", "PUT", "DELETE"])
@secure_route
def query_risk(email, risk_id):
    if request.method == "GET":

        risks = getFilteredRisksUseCase(current_app.config["REPOSITORY"], {"id": risk_id})
        if not isinstance(risks, Risk):
            return jsonify({"error": "The given risk does not exist"}), HttpCodes.NOT_FOUND.value
        
        return (
            jsonify(risks.asDict()),
            HttpCodes.OK.value,
        )

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        if not "name" in data and not "description" in data and not "probability" in data and not "impact" in data and not "provider_id" in data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        operation = updateRiskUseCase(
            current_app.config["REPOSITORY"],
            risk_id,
            {key:value for key,value in data.items() if key in ["name", "description", "probability", "impact", "provider_id"]}
        )
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify({"message": "Risk updated"}), HttpCodes.OK.value

    if request.method == "DELETE":
        operation = deleteRiskUseCase(current_app.config["REPOSITORY"], risk_id)
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return jsonify({"message": "Risk deleted"}), HttpCodes.NO_CONTENT.value

@bp.route("/profile", methods=["GET"])
@secure_route
def users(email):
    if request.method == "GET":
        user = getUserByEmailUseCase(current_app.config["REPOSITORY"], email)
        if isinstance(user, str):
            return jsonify({"error": user}), HttpCodes.INTERNAL_SERVER_ERROR.value

        return (
            jsonify(user.asDict()),
            HttpCodes.OK.value,
        )
    
@bp.route("/users/<int:user_id>/roles", methods=["GET", "POST", "DELETE"])
@secure_route
def user_roles(email, user_id):
    if request.method == "GET":
        user = getUserRolesUseCase(current_app.config["REPOSITORY"], user_id)
        if isinstance(user, str):
            return jsonify({"error": user}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return (
            jsonify(user.asDict()),
            HttpCodes.OK.value,
        )
    
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        if not "role_id" in data:
            return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

        operation = addRoleToUserUseCase(
            current_app.config["REPOSITORY"],
            user_id,
            data["role_id"],
        )
        if isinstance(operation, str):
            return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
        
        return jsonify({"message": "Role added"}), HttpCodes.CREATED.value

@bp.route("/users/<int:user_id>/roles/<int:role_id>", methods=["DELETE"])
@secure_route
def user_role(email, user_id, role_id):
    operation = removeRoleFromUserUseCase(
        current_app.config["REPOSITORY"],
        user_id,
        role_id
    )
    if isinstance(operation, str):
        return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
    
    return jsonify({"message": "Role removed"}), HttpCodes.OK.value
    
@bp.route("/risks/<int:risk_id>/users", methods=["POST"])
@secure_route
def user_risks(email, risk_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

    if not "user_id" in data:
        return jsonify({"error": "Invalid request"}), HttpCodes.BAD_REQUEST.value

    operation = addUserToRiskUseCase(
        current_app.config["REPOSITORY"],
        data["user_id"],
        risk_id,
    )
    if isinstance(operation, str):
        return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
    
    return jsonify({"message": "Risk added"}), HttpCodes.CREATED.value
    
@bp.route("/risks/<int:risk_id>/users/<int:user_id>", methods=["DELETE"])
@secure_route
def user_risk(email, risk_id, user_id):
    operation = removeUserFromRiskUseCase(
        current_app.config["REPOSITORY"],
        user_id,
        risk_id
    )
    if isinstance(operation, str):
        return jsonify({"error": operation}), HttpCodes.INTERNAL_SERVER_ERROR.value
    
    return jsonify({"message": "Risk removed"}), HttpCodes.OK.value

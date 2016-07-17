# base views
from config import SECRET_KEY, PASSWORD_RESET_EMAIL
from datetime import datetime, timedelta
from functools import wraps
from flask import g, Blueprint, jsonify, make_response, request
from flask_restful import Resource, Api
import flask_restful
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import jwt
from jwt import DecodeError, ExpiredSignature
from app.base_model import db
from app.employees.models import Employee, EmployeeSchema


login1 = Blueprint('login', __name__)
api = Api(login1)
schema = EmployeeSchema(strict=True)
mail = Mail()

# JWT AUTh process start


def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1),
        'scope': 'emp'
    }
    token = jwt.encode(payload, SECRET_KEY)
    return token.decode('unicode_escape')


def parse_token(req):

    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')

# Login decorator function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']"""

        return f(*args, **kwargs)

    return decorated_function


def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            # print(request.headers.get('Authorization'))
            payload = parse_token(request)
            if payload['scope'] != "admin":
                response = jsonify(error='Admin Access Required')
                response.status_code = 401
                return response
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function

# JWT AUTh process end

# Login Authentication Class


class Auth(Resource):

    def post(self):
        raw_dict = request.get_json(force=True)
        data = raw_dict['data']['attributes']
        email = data['email']
        password = data['password']
        user = Employee.query.filter_by(empEmail=email).first()
        if user is None:
            response = make_response(
                jsonify({"message": "invalid username/password"}))
            response.status_code = 401
            return response
        if check_password_hash(user.empPassword, password):

            token = create_token(user)
            return {'token': token}
        else:
            response = make_response(
                jsonify({"message": "invalid username/password"}))
            response.status_code = 401
            return response

api.add_resource(Auth, 'login.json')


class SignUp(Resource):

    def post(self):
        print('Signup start1')
        raw_dict = request.get_json(force=True)
        print('Signup start2')
        print(raw_dict)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
#           active = "false"
            print('Users prepared')
            user = Employee(
                request_dict['email'],
                generate_password_hash(request_dict['password']),
                request_dict['name'], request_dict['name'])
            print(user)
            user.add(user)
            print('user added')
            # Should not return password hash
            query = Employee.query.get(user.id)
            print('user queried')
            results = schema.dump(query).data
            print('schema dump')
            return results, 201

        except ValidationError as err:
            print('exception validation error')
            resp = jsonify({"error": err.messages})
            print(resp)
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


api.add_resource(SignUp, 'signup.json')


class ForgotPassword(Resource):

    def patch(self):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            print(request.headers.get('Authorization'))
            payload = parse_token(request)
            user_id = payload['sub']
            user = Employee.query.get_or_404(user_id)
            print(request.data)
            raw_dict = request.get_json(force=True)
            request_dict = raw_dict['data']['attributes']

            user.empPassword = generate_password_hash(request_dict['password'])
            try:
                user.update()
                return 201

            except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

    def post(self):
        request_dict = request.get_json(force=True)['data']['attributes']
        email = request_dict['email']
        user = Employee.query.filter_by(empEmail=email).first()
        if user is not None:
            token = create_token(user)
            msg = Message("Here's your Password Reset Link :)",
                          recipients=[email])
            msg.html = PASSWORD_RESET_EMAIL.format(token=token)
            mail.send(msg)
            return {"message": "Password reset mail sent successfully"}, 201
        else:
            return {"error": "We could not find this email address :("}, 404

api.add_resource(ForgotPassword, 'forgotpassword')

# Adding the login decorator to the Resource class


class Resource(flask_restful.Resource):
    method_decorators = [login_required]

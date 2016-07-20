from flask import Blueprint, request, jsonify, make_response
from app.employees.models import Employee, EmployeeSchema
from flask_restful import Api
from app.base_view import Resource
from app.base_model import db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

employees = Blueprint('employees', __name__)
schema = EmployeeSchema(strict=True)
api = Api(employees)


class EmployeeResource(Resource):

    def get(self):
        employees = Employee.query.order_by(Employee.firstName).all()
        results = schema.dump(employees, many=True).data
        return results

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']

            visaStartDate = None
            if('visaStartDate' in request_dict):
                visaStartDate = request_dict['visaStartDate']
            visaEndDate = None
            if('visaEndDate' in request_dict):
                visaEndDate = request_dict['visaEndDate']

            employee = Employee(request_dict['empEmail'],
                                request_dict['empPassword'],
                                request_dict['firstName'],
                                request_dict['lastName'],
                                None,
                                request_dict['empType'],
                                request_dict['timesheetType'],
                                request_dict['clientId'],
                                request_dict['clientName'],
                                request_dict['empStatus'],
                                request_dict['projectStatus'],
                                request_dict['visaType'],
                                visaStartDate, visaEndDate)

            employee.add(employee)
            # Should not return password hash
            query = Employee.query.get(employee.id)
            results = schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"TT_ERROR": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"TT_ERROR": str(e)})
            resp.status_code = 403
            return resp


class EmployeeUpdateResource(Resource):

    def get(self, id):
        employee = Employee.query.get_or_404(id)
        result = schema.dump(employee).data
        return result

    def patch(self, empId):
        employee = Employee.query.get_or_404(empId)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(employee, key, value)

            employee.update()
            return self.get(empId)

        except ValidationError as err:
            resp = jsonify({"TT_ERROR": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"TT_ERROR": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, empId):
        employee = Employee.query.get_or_404(empId)
        try:
            Employee.delete(employee)
            response = make_response()
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"TT_ERROR": str(e)})
            resp.status_code = 401
            return resp


api.add_resource(EmployeeResource, '/')
api.add_resource(EmployeeUpdateResource, '/<int:id>/')

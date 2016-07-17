from flask import current_app, Blueprint, request, jsonify, make_response
from app.timesheets.models import Timesheet, TimesheetSchema
from flask_restful import Api
from app.base_view import Resource
from app.base_model import db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError


timesheets = Blueprint('timesheets', __name__)
schema = TimesheetSchema(strict=True)
api = Api(timesheets)


class TimesheetResource(Resource):

    def get(self):
        clientId = request.args.get('clientId')
        status = request.args.get('status')
        page = request.args.get('page')
        if(page is None):
            page = 1
        current_app.logger.info('ClientId:%s, status:%s, page:%s',
                                clientId, status, page)

        query = Timesheet.query
        if(clientId is not None):
            query = query.filter(Timesheet.clientId == clientId)
        if(status is not None):
            query = query.filter(Timesheet.status == status)
#        timesheets = query.all()
        paginator = query.paginate(int(page), 10, False)
        timesheets = paginator.items
        totalCount = paginator.total
        print('total:', totalCount)
        results = schema.dump(timesheets, many=True).data
        results['totalCount'] = totalCount
        return results

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']

            timesheetId = None
            if('id' in raw_dict['data']):
                timesheetId = raw_dict['data']['id']
            approverId = None
            if('approverId' in request_dict):
                approverId = request_dict['approverId']

            timesheet = Timesheet(request_dict['empId'],
                request_dict['firstName'], request_dict['lastName'],
                request_dict['status'], request_dict['timesheetType'],
                timesheetId, approverId,
                request_dict['clientId'], request_dict['clientName'],
                request_dict['workHours'], request_dict['totalHours'],
                request_dict['startDate'], request_dict['endDate'],
                None, None)

            timesheet.add(timesheet)
            # Should not return password hash
            query = Timesheet.query.get(timesheet.id)
            results = schema.dump(query).data
            return results, 201

        except ValidationError as valerr:
            current_app.logger.error('ValidationError:%s', valerr)
            resp = jsonify({"TT_ERROR": valerr.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as sqlerr:
            current_app.logger.error('SQLAlchemyError:%s', sqlerr)
            db.session.rollback()
            resp = jsonify({"TT_ERROR": str(sqlerr)})
            resp.status_code = 403
            return resp


class TimesheetUpdateResource(Resource):

    def get(self, id):
        print('TimesheetUpdateResource.get')
        timesheet = Timesheet.query.get_or_404(id)
        result = schema.dump(timesheet).data
        return result

    def patch(self, id):
        timesheet = Timesheet.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(timesheet, key, value)

            timesheet.update()
            return self.get(id)

        except ValidationError as err:
            resp = jsonify({"TT_ERROR": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"TT_ERROR": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, id):
        timesheet = Timesheet.query.get_or_404(id)
        try:
            Timesheet.delete(timesheet)
            response = make_response()
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"TT_ERROR": str(e)})
            resp.status_code = 401
            return resp


api.add_resource(TimesheetResource, '/')
api.add_resource(TimesheetUpdateResource, '/<int:id>')

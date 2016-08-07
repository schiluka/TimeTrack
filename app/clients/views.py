from flask import Blueprint, request, jsonify, make_response
from app.clients.models import Client, ClientSchema
from flask_restful import Api
from app.base_view import Resource
from app.base_model import db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

clients = Blueprint('clients', __name__)
schema = ClientSchema(strict=True)
api = Api(clients)


class ClientResource(Resource):

    def get(self):
        clients = Client.query.order_by(Client.clientName).all()
        results = schema.dump(clients, many=True).data
        return results

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']

            client = Client(request_dict['clientName'],
                            request_dict['address'],
                            request_dict['city'],
                            request_dict['state'],
                            request_dict['zipCode'],
                            None)

            client.add(client)
            # Should not return password hash
            query = Client.query.get(client.id)
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


class ClientUpdateResource(Resource):

    def get(self, id):
        client = Client.query.get_or_404(id)
        result = schema.dump(client).data
        return result

    def patch(self, clientId):
        client = Client.query.get_or_404(clientId)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            for key, value in request_dict.items():
                setattr(client, key, value)

            client.update()
            return self.get(clientId)

        except ValidationError as err:
            resp = jsonify({"TT_ERROR": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"TT_ERROR": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, clientId):
        client = Client.query.get_or_404(clientId)
        try:
            Client.delete(client)
            response = make_response()
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"TT_ERROR": str(e)})
            resp.status_code = 401
            return resp


api.add_resource(ClientResource, '/')
api.add_resource(ClientUpdateResource, '/<int:id>/')

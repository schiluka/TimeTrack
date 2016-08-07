from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.base_model import db, BaseModel


class Client(db.Model, BaseModel):
    id = db.Column("clnt_id", db.Integer, primary_key=True, autoincrement=True)
    clientName = db.Column("clnt_nam", db.String(200), nullable=False)
    address = db.Column("clnt_addr", db.String(200), nullable=False)
    city = db.Column("clnt_cty", db.String(50), nullable=False)
    state = db.Column("clnt_ste", db.String(50), nullable=False)
    zipCode = db.Column("clnt_zip", db.String(20), nullable=False)

    def __init__(self, clientName, address, city, state, zipCode, id=None):
        self.id = id
        self.clientName = clientName
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zipCode


class ClientSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(as_string=True, dump_only=True)
    clientName = fields.String(validate=not_blank)
    address = fields.String(validate=not_blank)
    city = fields.String(validate=not_blank)
    state = fields.String(validate=not_blank)
    zipCode = fields.String(validate=not_blank)

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/clients/"
        else:
            self_link = "/clients/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'clients'

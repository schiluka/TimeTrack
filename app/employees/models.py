from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.base_model import db, BaseModel


class Employee(db.Model, BaseModel):
    id = db.Column("emp_id", db.Integer, primary_key=True, autoincrement=True)
    empEmail = db.Column("emp_email", db.String(100), nullable=False)
    empPassword = db.Column("emp_pswd", db.String(50), nullable=False)
    firstName = db.Column("fst_nam", db.String(100), nullable=False)
    lastName = db.Column("lst_nam", db.String(100), nullable=False)
    empType = db.Column("emp_typ", db.String(10), nullable=False)
    timesheetType = db.Column("ts_typ", db.String(10), nullable=False)
    clientId = db.Column("clnt_id", db.String(10), nullable=True)
    clientName = db.Column("clnt_nam", db.String(50), nullable=True)
    empStatus = db.Column("emp_sta", db.String(10), nullable=False)
    projectStatus = db.Column("proj_sta", db.String(10), nullable=True)
    visaType = db.Column("visa_typ", db.String(20), nullable=False)
    visaStartDate = db.Column("visa_sta_dt", db.Date, nullable=True)
    visaEndDate = db.Column("visa_end_dt", db.Date, nullable=True)

    def __init__(self, empEmail, empPassword, firstName, lastName,
                 id=None, empType=None, timesheetType=None, clientId=None,
                 clientName=None, empStatus=None, projectStatus=None,
                 visaType=None, visaStartDate=None, visaEndDate=None):
        self.id = id
        self.empEmail = empEmail
        self.empPassword = empPassword
        self.firstName = firstName
        self.lastName = lastName
        self.empType = empType
        self.timesheetType = timesheetType
        self.clientId = clientId
        self.clientName = clientName
        self.empStatus = empStatus
        self.projectStatus = projectStatus
        self.visaType = visaType
        self.visaStartDate = visaStartDate
        self.visaEndDate = visaEndDate


class EmployeeSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(as_string=True, dump_only=True)
    empEmail = fields.Email(validate=not_blank)
    # empPassword = fields.String(validate=not_blank)
    firstName = fields.String(validate=not_blank)
    lastName = fields.String(validate=not_blank)
    empType = fields.String(validate=not_blank)
    timesheetType = fields.String()
    clientId = fields.String()
    clientName = fields.String()
    empStatus = fields.String(validate=not_blank)
    projectStatus = fields.String(validate=not_blank)
    visaType = fields.String()
    visaStartDate = fields.DateTime()
    visaEndDate = fields.DateTime()

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/employees/"
        else:
            self_link = "/employees/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'employees'

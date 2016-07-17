from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.base_model import db, BaseModel


class Employee(db.Model, BaseModel):
    id = db.Column("emp_id", db.Integer, primary_key=True)
    empEmail = db.Column("emp_email", db.String(100), nullable=False)
    empPassword = db.Column("emp_pswd", db.String(50), nullable=False)
    firstName = db.Column("fst_nam", db.String(100), nullable=False)
    lastName = db.Column("lst_nam", db.String(100), nullable=False)
    userType = db.Column("emp_typ", db.String(10), nullable=False)
    timesheetType = db.Column("ts_typ", db.String(10), nullable=False)
    clientId = db.Column("clnt_id", db.String(10), nullable=True)
    clientName = db.Column("clnt_nam", db.String(50), nullable=True)
    empStatus = db.Column("emp_sta", db.String(10), nullable=False)
    projectStatus = db.Column("proj_sta", db.String(10), nullable=True)
    visaType = db.Column("visa_typ", db.String(20), nullable=False)
    visaStartDate = db.Column("visa_sta_dt", db.DateTime, nullable=True)
    visaEndDate = db.Column("visa_end_dt", db.DateTime, nullable=True)

    def __init__(self, empEmail, empPassword, firstName, lastName,
                 userType=None, timesheetType=None, clientId=None,
                 clientName=None, empStatus=None, projectStatus=None,
                 visaType=None, visaStartDate=None, visaEndDate=None):

        self.empEmail = empEmail
        self.empPassword = empPassword
        self.firstName = firstName
        self.lastName = lastName
        self.userType = userType
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
    id = fields.Integer(dump_only=True)
    empEmail = fields.Email(validate=not_blank)
    empPassword = fields.String(validate=not_blank)
    firstName = fields.String(validate=not_blank)
    lastName = fields.String(validate=not_blank)
    userType = fields.String(validate=not_blank)
    timeSheetType = fields.String(validate=not_blank)
    clientId = fields.String()
    clientName = fields.String()
    empStatus = fields.String()
    projectStatus = fields.String()
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

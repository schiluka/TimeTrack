from sqlalchemy.sql import func
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.base_model import db, BaseModel


class Timesheet(db.Model, BaseModel):
    id = db.Column("ts_id", db.Integer, primary_key=True, autoincrement=True)
    empId = db.Column("emp_id", db.Integer, nullable=False)
    firstName = db.Column("fst_nam", db.String(100), nullable=False)
    lastName = db.Column("lst_nam", db.String(100), nullable=False)
    timesheetType = db.Column("ts_typ", db.String(10), nullable=False)
    approverId = db.Column("appr_id", db.Integer, nullable=True)
    clientId = db.Column("clnt_id", db.String(10), nullable=True)
    clientName = db.Column("clnt_nam", db.String(100), nullable=True)
    status = db.Column("ts_sta", db.String(10), nullable=False)
    workHours = db.Column("wrk_hrs", db.String(150), nullable=False)
    totalHours = db.Column("total_hrs", db.Integer, nullable=False)
    startDate = db.Column("start_dt", db.Date, nullable=True)
    endDate = db.Column("end_dt", db.Date, nullable=True)
    submitDate = db.Column("sub_dt", db.Date,
                           default=func.current_date(),
                           nullable=True)
    approveDate = db.Column("appr_dt", db.Date, nullable=True)

    def __init__(self, empId, firstName, lastName, status,
                 timesheetType, id=None, approverId=None, clientId=None,
                 clientName=None, workHours=None, totalHours=None,
                 startDate=None, endDate=None, submitDate=None,
                 approveDate=None):
        self.id = id
        self.empId = empId
        self.firstName = firstName
        self.lastName = lastName
        self.timesheetType = timesheetType
        self.approverId = approverId
        self.clientId = clientId
        self.clientName = clientName
        self.status = status
        self.workHours = workHours
        self.totalHours = totalHours
        self.startDate = startDate
        self.endDate = endDate
        self.submitDate = submitDate
        self.approveDate = approveDate


class TimesheetSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(as_string=True, dump_only=True)
    empId = fields.Integer(as_string=True, dump_only=True)
    firstName = fields.String(validate=not_blank)
    lastName = fields.String(validate=not_blank)
    userType = fields.String(validate=not_blank)
    timesheetType = fields.String(validate=not_blank)
    approverId = fields.Integer(as_string=True, dump_only=True)
    clientId = fields.String()
    clientName = fields.String()
    status = fields.String(validate=not_blank)
    workHours = fields.String(validate=not_blank)
    totalHours = fields.Integer(as_string=True, dump_only=True)
    startDate = fields.Date()
    endDate = fields.Date()
    submitDate = fields.Date()
    # approveDate = fields.DateTime()

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/timesheets/"
        else:
            self_link = "/timesheets/{}".format(data['id'])
        return {'self': self_link}

    # def unwrap_item(self, item):
        # Overload this function from marshmallow-jsonapi so it
        # actually stores the id.
        # Work around for ma-jsonapi requiring attributes when loading data.
        # if 'attributes' not in item:
        #    item['attributes'] = {}
        # payload = super().unwrap_item(item)
        # Work around for ma-jsonapi not loading the ids
        # payload['id'] = item['id']
        # return payload

    class Meta:
        type_ = 'timesheets'

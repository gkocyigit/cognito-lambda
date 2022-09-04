from email.policy import default
from datetime import datetime
from dynamorm import DynaModel, GlobalIndex, ProjectAll

from marshmallow import fields, validate, validates, ValidationError

class Account(DynaModel):
    class Table:
        name = 'account'
        hash_key = 'username'

    class Schema:
        image_id = fields.String(validate=validate.Length(0,200))
        date_created = fields.DateTime(default=datetime.now())
        is_recurring = fields.Bool()
        email_verified_at= fields.String(validate=validate.Length(0,200))
        first_name= fields.String(validate=validate.Length(0,200),default="Test")
        last_name= fields.String(validate=validate.Length(0,200),default="Test")
        fullname= fields.String(validate=validate.Length(0,200))
        phone_number= fields.String(validate=validate.Length(0,14))
        profile_type= fields.String(validate=validate.Length(0,200))
        balance= fields.String(validate=validate.Length(0,200))
        tenant_id= fields.String(validate=validate.Length(0,200))
        promo_code= fields.String(validate=validate.Length(0,200))
        formatted_date= fields.String(validate=validate.Length(0,200))
        account_number= fields.String(validate=validate.Length(0,10))
        father_name= fields.String(validate=validate.Length(0,200))
        status= fields.String(validate=validate.Length(0,200))
        address= fields.String(validate=validate.Length(0,200))
        dob= fields.String(validate=validate.Length(0,200))
        city= fields.String(validate=validate.Length(0,200))
        gender= fields.String(validate=validate.Length(0,200))
        rating= fields.String(validate=validate.Length(0,200))
        state= fields.String(validate=validate.Length(0,200))
        country= fields.String(validate=validate.Length(0,200))
        delete_flag = fields.Bool(default=False)
        last_logged_in = fields.DateTime(default=datetime.now())
        last_modified = fields.DateTime(default=datetime.now())
        bvn= fields.String(validate=validate.Length(0,14))
        pin= fields.String(validate=validate.Length(0,14))
        question_1= fields.String(validate=validate.Length(0,200))
        question_2= fields.String(validate=validate.Length(0,200))
        question_3= fields.String(validate=validate.Length(0,200))
        answer_1= fields.String(validate=validate.Length(0,200))
        answer_2= fields.String(validate=validate.Length(0,200))
        answer_3= fields.String(validate=validate.Length(0,200))
        docType= fields.String(validate=validate.Length(0,200))
        last_login = fields.DateTime(default=datetime.now())
        date_joined = fields.DateTime(default=datetime.now())
        is_superuser = fields.Bool(default=False)
        is_staff = fields.Bool(default=False) 
        is_active = fields.Bool(default=False) 
        username= fields.String(validate=validate.Length(0,200),required=True)
        countryCode= fields.String(validate=validate.Length(0,200))
        receive_notifications = fields.Bool(default=True)
        date_of_birth= fields.String(validate=validate.Length(0,200))
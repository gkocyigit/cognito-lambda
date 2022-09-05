import os
import awsgi
import boto3
import sys
import traceback
import json
import time
import urllib.request

from dotenv import load_dotenv
from jose import jwk, jwt
from jose.utils import base64url_decode
from dynamorm.exceptions import ValidationError
from pydantic.error_wrappers import ValidationError as PydanditValidationError
from datetime import datetime
from flask import (
    Flask,
    jsonify,
    request,
    json
)
from models.responses import AccountDetailResponse
from models.requests import CreateAccountRequest
from models.account import Account

app = Flask(__name__)

load_dotenv()

cognito_client=boto3.client('cognito-idp')

region = os.environ["AWS_REGION"]
userpool_id = os.environ["COGNITO_USER_POOL_ID"]
app_client_id = os.environ["COGNITO_APP_CLIENT_ID"]
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

with urllib.request.urlopen(keys_url) as f:
  response = f.read()
keys = json.loads(response.decode('utf-8'))['keys']

@app.route('/login',methods=["POST"])
def login():
    try:
        data = json.loads(request.data)

        if "email" not in data or "password" not in data:
            return (jsonify(message='Email or Password missing'),400)

        res=cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                "USERNAME":data["email"],
                "PASSWORD":str(data["password"])
            },
            ClientId=app_client_id,
        )

        # For simplicity
        if "ChallengeName" in res and res["ChallengeName"]=="NEW_PASSWORD_REQUIRED":
            challengeResponse = cognito_client.respond_to_auth_challenge(
                ChallengeName='NEW_PASSWORD_REQUIRED',
                ClientId=app_client_id,
                ChallengeResponses={
                    "USERNAME":data["email"],
                    "NEW_PASSWORD":str(data["password"])
                },
                Session=res["Session"]
            )

            token=challengeResponse["AuthenticationResult"]["AccessToken"]
        else :
            token = res["AuthenticationResult"]["AccessToken"]

        return {
            "token":token
        }
    except cognito_client.exceptions.UserNotFoundException as e:
        return (jsonify(message='User not found'),404)
    except cognito_client.exceptions.NotAuthorizedException as e:
        return (jsonify(message='Incorrect username or password'),400)
    except Exception as e:
        print(repr(e))
        traceback.print_tb(sys.exc_info()[2])
        return (jsonify(message='Internal Server Error'),500)

@app.route('/create',methods=["POST"])
def create_account():
    try:
        data = json.loads(request.data)
        data = CreateAccountRequest(**data)

        account = Account(
            username= data.username,
            image_id = data.image_id,
            date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            is_recurring = data.is_recurring,
            email_verified_at= data.email_verified_at,
            first_name= data.first_name,
            last_name= data.last_name,
            fullname= data.fullname,
            phone_number= data.phone_number,
            profile_type= data.profile_type,
            balance= data.balance,
            tenant_id= data.tenant_id,
            promo_code= data.promo_code,
            formatted_date= data.formatted_date,
            account_number= data.account_number,
            father_name= data.father_name,
            status= data.status,
            address= data.address,
            dob= data.dob,
            city= data.city,
            gender= data.gender,
            rating= data.rating,
            state= data.state,
            country= data.country,
            delete_flag = data.delete_flag,
            last_logged_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            bvn= data.bvn,
            pin= data.pin,
            question_1= data.question_1,
            question_2= data.question_2,
            question_3= data.question_3,
            answer_1= data.answer_1,
            answer_2= data.answer_2,
            answer_3= data.answer_3,
            docType= data.docType,
            last_login = data.last_login,
            date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            is_superuser = data.is_superuser,
            is_staff = data.is_staff,
            is_active = data.is_active,
            countryCode= data.countryCode,
            receive_notifications = data.receive_notifications,
            date_of_birth= data.date_of_birth,
        )

        queryAccountRes=Account.query(username=data.username)

        if queryAccountRes.count()>0:
            return (jsonify(message='User exists'),404)

        cognito_client.admin_create_user(
            UserPoolId=userpool_id,
            Username=data.username,
            TemporaryPassword=data.password,
            UserAttributes=[
                {
                    "Name":"email",
                    "Value":data.username
                },
            ],
            MessageAction="SUPPRESS"
        )

        #Save the account details in DynamoDB
        account.save()

        return {
            "success":True
        }
    except PydanditValidationError as e:
        print(repr(e))
        traceback.print_tb(sys.exc_info()[2])
        return (jsonify(message='Request not valid'),404)
    except ValidationError as e:
        print(repr(e))
        traceback.print_tb(sys.exc_info()[2])
        return (jsonify(message='Request not valid'),404)
    except Exception as e:
        print(repr(e))
        traceback.print_tb(sys.exc_info()[2])
        return (jsonify(message='Internal Server Error'),500)


@app.route('/account-detail',methods=["GET"])
def account_detail():
    try:
        authToken = request.headers["Authorization"].split()[1]
        if verify_jwt_token(authToken) == False: 
            return (jsonify(message='Unauthorized'),401)

        user=cognito_client.get_user(AccessToken=authToken)

        queryAccountRes=Account.query(username=user["Username"]).specific_attributes([
            "first_name",
            "last_name",
            "fullname",
            "phone_number",
            "profile_type",
            "balance",
            "tenant_id",
            "promo_code",
            "formatted_date",
            "account_number",
            "father_name",
            "status",
            "address",
            "dob",
            "city",
            "gender",
            "rating",
            "state",
            "country"
        ])
        
        userAccount=next(queryAccountRes)
        
        response=AccountDetailResponse(
            first_name=userAccount.first_name,
            last_name =userAccount.last_name,
            fullname =userAccount.fullname,
            phone_number=userAccount.phone_number,
            profile_type=userAccount.profile_type,
            balance=userAccount.balance,
            tenant_id=userAccount.tenant_id,
            promo_code=userAccount.promo_code,
            formatted_date=userAccount.formatted_date,
            account_number=userAccount.account_number,
            father_name=userAccount.father_name,
            status=userAccount.status,
            address=userAccount.address,
            dob=userAccount.dob,
            city=userAccount.city,
            gender=userAccount.gender,
            rating=userAccount.rating,
            state=userAccount.state,
            country=userAccount.country,
        )

        return (response.dict(),200)
    except cognito_client.exceptions.NotAuthorizedException as e:
        print(repr(e))
        traceback.print_tb(sys.exc_info()[2])
        return (jsonify(message='Unauthorized'),401)
    except Exception as e:
        print(repr(e))
        traceback.print_tb(sys.exc_info()[2])
        return (jsonify(message='Internal Server Error'),500)

def verify_jwt_token(token):
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']

    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False

    public_key = jwk.construct(keys[key_index])
    
    message, encoded_signature = str(token).rsplit('.', 1)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    return True
   
def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
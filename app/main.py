from email import message
import awsgi
from flask import (
    Flask,
    jsonify,
    request,
    json
)
import boto3

from models.account import Account

app = Flask(__name__)

cognito_client=boto3.client('cognito-idp')

@app.route('/login',methods=["POST"])
def login():
    try:
        data = json.loads(request.data)

        res=cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                "USERNAME":data["email"],
                "PASSWORD":str(data["password"])
            },
            ClientId="75nouu1kqjhvqlbiiasd6dgpld",
        )

        # For simplicity
        if "ChallangeName" in res and res["ChallangeName"]=="NEW_PASSWORD_REQUIRED":
            challengeResponse = cognito_client.respond_to_auth_challenge(
                ChallengeName='NEW_PASSWORD_REQUIRED',
                ClientId="75nouu1kqjhvqlbiiasd6dgpld",
                ChallengeResponses={
                    "USERNAME":data["email"],
                    "NEW_PASSWORD":str(data["password"])
                },
                Session=res["Session"]
            )

            token=challengeResponse["AuthenticationResult"]["AccessToken"]
        else :
            token = res["AuthenticationResult"]["AccessToken"]


        return jsonify(
            status=200,
            response={
                "token":token
            }
        ) 

    except Exception as e:
        print(e)
        return jsonify(status=500, message='Internal Server Error')

@app.route('/create')
def create_account():
    return jsonify(status=200, message='TEST OK')


def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
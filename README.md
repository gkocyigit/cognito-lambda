# cognito-lambda

A Flask Application that uses Amazon Cognito, AWS DynamoDB and AWS Lambda

## Local Running

This application can be run on your local with:
```
python .\app\main.py
```
assuming you have the right aws credentials in the default profile

## Endpoints

There are 3 endpoints: 
- POST /login : Logs in the user with the given `email` and `password` using Cognito
- POST /create : Creates the account in Cognito and creates account in DynamoDB with the given `data`
- GET /account-detail: Authenticates the user from Cognito using `Authorization` header and returns the account details from DynamoDB

Sample requests are added as a postman collection in `postman-collection.json` file

## Deploying

```
sam build --use-container
sam deploy
```
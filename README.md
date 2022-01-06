# Amazon Lambda function to insert user data into AWS RDS Oracle database.
This project contains source code and supporting files for a python based Amazon lambda function to insert data
into Oracle database. API GW endpoint is created to allow user to send data in payload request. 

This is a sample application to store user information (ID, FirstName, LastName) into Oracle database 
table called "users". Input user data will be sent through API endpoint in the form of payload.

Sample Payload Request JSON:
  {'data': [{'id' : 1, first_name': 'F1', 'last_name': 'L1'}]}


## Pre-requsites
- Create oracle database using Amazon RDS service.
- Create table "users" with columns "id,first_name,last_name"
- Oracle DB creation and table creation is not part of current SAM template. It can be enhanced later.


## Features
- Lambda function and API GW environment can be deployed using SAM template.
- User can pass input record as a payload request in API endpoint "users" using "POST" method.
- New user information will be inserted once post mehod trigerred and then all available records will be displayed in response.


## Tech
Below are list of technologies used.
- [Python] - Python script is written to create AMI snapshot manager application.
- [boto3] - Python boto3 SDK used to interact with AWS services.
- [cx_Oracle] - Library used to interact with Oracle database.

Below are list of AWS services used in this project.
- [RDS]     - Boto3 client object used to interact with Oracle RDS instance.
- [Lambda]  - AWS Lambda function created.


## Package installation steps

User should use below command to create this package.
```bash
sam package --region $AWSRegion --profile $ProfileName --s3-bucket $BucketName --template-file $BuiltTemplate --output-template-file deploy.yaml
```

User should use below command to deploy this package.
```bash
sam deploy --region $AWSRegion --profile $ProfileName --s3-bucket $BucketName --template-file $BuiltTemplate --stack-name $StackName --capabilities CAPABILITY_IAM

```


## License
MIT

**Free Software, Keep Learning!**

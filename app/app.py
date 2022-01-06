  #************************************************************************
## Lambda Function  : aws-apigw-oracle-data-insert
## Description      : Lambda function to load data into oracle using API GW
## Author           :
## Copyright        : Copyright 2021
## Version          : 1.0.0
## Mmaintainer      :
## Email            :
## Status           : In Review
##************************************************************************
## Version Info:
## 1.0.0 : 23-Sep-2021 : Created first version to load data into oracle
#                        Send record as a payload through API GW endpoint.
##************************************************************************
import sys, os, json
import boto3
from botocore.exceptions import ClientError
import traceback
from datetime import datetime, timedelta, date
import cx_Oracle
from docutils.nodes import row

# ***********************************************************************
# Global Db detail
# ***********************************************************************
db_user = 'admin'
db_pwd  = 'admin'
host    = 'admindb.abcdefghijkl.us-east-1.rds.amazonaws.com'
db_name = 'TESTDB'

##***********************************************************************
## Class Definition
##***********************************************************************
class APIDataLoader:
  #************************************************************************
  # Class constructor
  # {'data': [{'id' : 1, first_name': 'F1', 'last_name': 'L1'}]}
  #************************************************************************
  def __init__(self, data):
    self.record         = {}
    self.init(data)
    return

  # ************************************************************************
  # Function to initiate request
  # ************************************************************************
  def init(self, dataStr):
    if type(dataStr) == str:
      dataStr = dataStr.replace("\'", "\"")
      data = json.loads(dataStr)
    else:
      data = dataStr
    self.data = data
    return True

  # ************************************************************************
  # Function to run main logic
  # ************************************************************************
  def run(self):
    if self.is_valid_request():
      response = self.load_data()
    return response

  # ************************************************************************
  # Function to load data into oracle DB
  # ************************************************************************
  def load_data(self):
    response = {}
    if self.data:
      try:
        dns = "{}/{}@{}/{}".format(db_user,db_pwd,host,db_name)
        connection = cx_Oracle.connect(dns)
        cursor = connection.cursor()

        rows = []
        # Load all data
        for record in self.data:
          row = (record['first_name'], record['last_name'])
          rows.append(row)

        cursor.executemany("insert into users(first_name, last_name) values (:1, :2)", rows)
        connection.commit()
        print("Insert completed")

        # select and return data
        query = "select * from users"
        cursor.execute(query)
        response = cursor.fetchall()

        cursor.close()
      except Exception as e:
        print("Connection Exception :", e)

    resp = self.get_response(response)
    return resp

  #************************************************************************
  # Setup environment parameters if exists
  #************************************************************************
  def is_valid_request(self):
    rc = True
    if self.data:
      pass
    else:
      rc = False
      raise RuntimeError('Required parameters are missing in input request. Abort processing.')
    return rc

  def get_response(self, result):
    statusCode = 200
    headers = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    responseBody = { 'Response' : 'Success', 'result' : result }
    response = {
          "statusCode": statusCode,
          "headers": headers,
          "body": responseBody,
          "isBase64Encoded": False
      }
    return response

#************************************************************************
# main lambda handler
#************************************************************************
def lambda_handler(event, context):
  response = {}
  print("INFO :: Lambda function executon initiated")
  if 'data' in event:
    try:
      ADL = APIDataLoader(event['data'])
      response = ADL.run()
      print("Lambda Execution Status :")
    except Exception as inst:
      print("Error:: Unable to process request:", inst)
      traceback.print_exc()
  else:
    error_message = "Required key 'data' is missing in request. Abort processing."
    raise RuntimeError(error_message)
  print("INFO :: Lambda function executon completed")
  return response

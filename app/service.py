from app import app
from math import radians, cos, sin, asin, sqrt
from flask import request, url_for
from database.crud import get_filtered_customers, select_data, update_data, get_filtered_products, get_filtered_orders
from marshmallow import (
    Schema,fields,validate)
import json
import os
from datetime import datetime, timedelta
from app import db

HTTP_INVALID_REQUEST = 400

class InputSchema(Schema):
  """ function to validate input params"""
  limitMax = int(os.environ.get('API_RESPONSE_LIMIT')) if "API_RESPONSE_LIMIT" in os.environ else 100   
  radiusMax = int(os.environ.get('RADIUS_MAX_VALUE')) if "RADIUS_MAX_VALUE" in os.environ else 10 

  subscriptionKey = fields.Str(data_key="subscription-key",validate=[validate.Length(min=1)])
  locationId = fields.Str(validate=[validate.Length(min=4)])
  latitude = fields.Float(validate=[validate.Range(min=-180,min_inclusive=True,max=180,max_inclusive=True)])
  longitude = fields.Float(validate=[validate.Range(min=-180,min_inclusive=True,max=180,max_inclusive=True)])
  zipCode = fields.Int(validate=[validate.Range(min=10,max=99999,error="Length must be greater than or equal to 2 and less than or equal to 5.")])
  locationName = fields.Str(validate=[validate.Length(min=5)])
  address = fields.Str(validate=[validate.Length(min=5)])
  radius = fields.Float(validate=[validate.Range(min=0,min_inclusive=False,max=radiusMax,max_inclusive=True)])
  limit = fields.Int(validate=[validate.Range(min=1,max=limitMax)])
  requestid = fields.Str(validate=[validate.Length(min=4)])
  rel = fields.Str(validate=[validate.Length(min=4)])
  _ref = fields.Str(validate=[validate.Length(min=1)])


def customers_data():
  """ this function is used to validate the input params and send relevant responses"""
  # schema = InputSchema()
  # errors = {}  
  # if len(request.args) > 0:
  #   validationerr = schema.validate(request.args)  
  #   if validationerr:
  #     errors = error_msg_handler(validationerr, HTTP_INVALID_REQUEST)      
  #   elif not errors:
  #     errors = validate_lat_longs(request.args.get('latitude'), request.args.get('longitude'))
  # else:
  #   errors = error_msg_handler("Need atleast one input parameter", HTTP_INVALID_REQUEST)  

  # if errors:
  #   return errors, {}

  try:
    response = get_customers(dict(request.args))
    
    return response
  except ValueError as e:
    app.logger.info("Something went wrong, unable to fetch locations data."+str(e))
    errors = error_msg_handler("Something went wrong, unable to fetch locations data.", HTTP_INVALID_REQUEST)  
    return errors


def error_msg_handler(error_msg, status_code):
    """Handle error message and return"""
    err = {}
    err['errors'] = error_msg
    err['status_code'] = status_code
    return err
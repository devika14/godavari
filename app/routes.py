from app import app
from flask import jsonify, request, make_response
from database.crud import get_filtered_customers, get_filtered_orders, get_filtered_products

@app.route("/customers", methods=['GET'])
def customers(): 
  """ route to get filtered customers"""
  response = get_filtered_customers()    
  return make_response(jsonify(response))   

@app.route("/orders", methods=['GET'])
def orders(): 
  """ route to get filtered orders"""
  response = get_filtered_orders()    
  return make_response(jsonify(response))   

@app.route("/products", methods=['GET'])
def products(): 
  """ route to get filtered products"""
  response = get_filtered_products()    
  return make_response(jsonify(response))       

# Used to debug all request with responses
@app.after_request
def after(response):
  """ log the request with its response"""
  app.logger.info('request: ' + str(request.url) +' , response status: ' + response.status + ', response data ' + response.data.decode('utf-8'))
  return response
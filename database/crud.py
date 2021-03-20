""" this module is for performing database crud operations"""
from sqlalchemy import create_engine, Table, Column, MetaData, Boolean, DateTime, Text, insert, String, Integer
from sqlalchemy.sql import text, and_
import os
from datetime import datetime, timedelta

from sqlalchemy.dialects import postgresql

meta = MetaData()
customers_table = Table(
    'customers', meta,
    Column('id', String(20), primary_key=True),
    Column('customer_name', String(500)),
    Column('customer_alt_contact', String(20)),
    Column('address', String(20)),
    Column('pincode', String(20)),
    Column('city', String(500)),
    Column('mobile', String(500)),
    Column('alt_mobile', String(45)),
    Column('email', String(45)),
    Column('community', String(45)),
    Column('created_by', String(45)),
    Column('updated_by', String(45)),
    Column('created_at', String(20)),
    Column('updated_at', String(20))
)

def get_filtered_customers(**kwargs):
  """" get the filtered customers from database"""
  
  response = []
  try:
    engine = create_db_engine()
    db_conn = engine.connect()
    with  db_conn as connection:
      rows = connection.execute("select * from customers")
      res = generate_response(rows)
      

      return res
      
      #response = generate_api_response(rows)
      db_conn.close()      
  except Exception as e:
    print("get customers data engne exce---*******************"+str(e))
    raise ValueError

  return response  

def get_filtered_products(**kwargs):
  """" get the filtered products from database"""
  
  response = []
  try:
    engine = create_db_engine()
    db_conn = engine.connect()
    with  db_conn as connection:
      rows = connection.execute("select * from products")
      response_list = []
      for row in rows:
        res = {}
        loc = dict(row)
        res['id'] = loc.get('id')
        res['product_id'] = loc.get('product_id')
        res['product_name'] = loc.get('product_name')
        res['mrp'] = loc.get('mrp')
        res['units'] = loc.get('units')
        res['purchase_price'] = loc.get('purchase_price')
        res['selling_price'] = loc.get('selling_price')
        res['stock'] = loc.get('stock')
        res['quantity'] = loc.get('quantity')
        
        response_list.append(res)
      return response_list
      
      #response = generate_api_response(rows)
      db_conn.close()      
  except Exception as e:
    print("get products data engne exce---*******************"+str(e))
    raise ValueError


def get_filtered_orders(**kwargs):
  """" get the filtered orders from database"""
  


  response = []
  try:
    engine = create_db_engine()
    db_conn = engine.connect()
    with  db_conn as connection:
      rows = connection.execute("select * from orders")
      response_list = []
      for row in rows:
        res = {}
        loc = dict(row)
        res['id'] = loc.get('id')
        res['order_id'] = loc.get('order_id')
        res['product_id'] = loc.get('product_id')
        res['customer_id'] = loc.get('customer_id')
        res['order_date'] = loc.get('order_date')
        res['quantity'] = loc.get('quantity')
        res['units'] = loc.get('units')
        res['rate'] = loc.get('rate')
        res['discount'] = loc.get('discount')
        res['tax'] = loc.get('tax')
        res['total_amount'] = loc.get('total_amount')
        res['payment_status'] = loc.get('payment_status')
        res['order_status'] = loc.get('order_status')
        res['description'] = loc.get('description')
        res['delivery_date'] = loc.get('delivery_date')
        res['payment_type'] = loc.get('payment_type')
        
        response_list.append(res)
      return response_list
      
      #response = generate_api_response(rows)
      db_conn.close()      
  except Exception as e:
    print("get products data engne exce---*******************"+str(e))
    raise ValueError



def generate_response(rows):
  """" map API response fields with db result"""
  response_list = []
  for row in rows:
    res = {}
    loc = dict(row)
    res['id'] = loc.get('id')
    res['customer_name'] = loc.get('customer_name')
    res['customer_alt_contact'] = loc.get('customer_alt_contact')
    res['address'] = loc.get('address')
    res['city'] = loc.get('city')
    res['pincode'] = loc.get('pincode')
    res['mobile'] = loc.get('mobile')
    res['alt_mobile'] = loc.get('alt_mobile')
    res['email'] = loc.get('email')
    res['community'] = loc.get('community')
    
    response_list.append(res)
  return response_list

def create_db_engine():
  """" creates db connection""" 
  try:
    return create_engine('mysql+pymysql://root:root@localhost:3306/godavari')
  except Exception as e:
    print('not connected')

def select_data(requestid):
  """ Select snapshot data from pagination  """
  connection = None
  if requestid is not None:            
    try:
      engine = create_db_engine()
      connection = engine.connect()
      with engine.connect() as connection:
        result = connection.execute(customers_table.select())
        response_list = []
        for row in result:
            res = {}
            pag = dict(row)
            res['id'] = pag.get('id')
            
            
            response_list.append(res)
          
        return response_list   
    except Exception as e:
      e.args = ("Something went wrong, unable to select new snapshot data ",) + e.args
      raise e
    finally:
      if connection is not None:
        connection.close()  


def update_data(before_id,after_id,_ref, requestid):
  """ Update snapshot for pagination link """
  connection = None
  try:
    engine = create_db_engine()
    connection = engine.connect()
    with engine.connect() as connection:
      now = datetime.now()
      start_date = now.strftime("%Y-%m-%d %H:%M:%S")
      add_time = now + timedelta(minutes=5)
      expiry_time = format(add_time, '%Y-%m-%d %H:%M:%S')
      update_query = snapshot_table.update().values(before_id=before_id,
                                                        after_id=after_id, start_time=start_date, expiry_time=expiry_time, ref_from=_ref).where(snapshot_table.c.requestid == requestid)
      connection.execute(update_query)
  except Exception as e:
    e.args = ("Something went wrong, unable to update new snapshot data ",) + e.args
    raise e
  finally:
    if connection is not None:
      connection.close()
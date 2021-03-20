from app import app

# def get_customers():
#     """ function to get filtered customers"""
#     try:
#       result = customers_data()
#       if 'errors' in result:
#         status_code = result.get('status_code')
#         result.pop('status_code')          
#         return result
#       else:
#         response = {}         
#         if len(result) == 0: 
#           response['data'] = []
#         else: 
#           response['data'] = result
       
#         return response['data']
#     except Exception as e:
#       app.logger.info("Failed to fetch customers data - "+ str(e))
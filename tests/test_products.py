
import unittest
import json
import sys
from application.database import conn,create_tables,delete_tables
from application.app import create_app



CREATE_PRODUCT_URL = '/api/v1/products/'
GET_SINGLE_PRODUCT = '/api/v1/product/1/'
GET_ALL_PRODUCTS = '/api/v1/products/'


class ProductTestCase(unittest.TestCase):

    def setUp(self):
        '''Initialize app and define test variables'''
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.products = { "name": "name", "quantity": 68, "min_stock":68, "price":2000, "category_id":1 }                              
        self.empty_products_name = {  "name": "", "quantity": 68, "min_stock":68, "price":2000, "category_id":1}
        self.empty_price = {  "name": "name", "quantity": 68, "min_stock":68, "price":"", "category_id":1 }
        self.empty_min_stock = {  "name": "name", "quantity": 68, "min_stock":"", "price":400, "category_id":1 }
        self.empty_quantity = {"name": "name", "quantity":"", "min_stock":3344, "price":400, "category_id":1 }
        self.login_user = { "email": "testproduct@gmail.com", "password":"12345678" }

        create_tables()
 

    def login(self):
        res_login = self.client.post('/api/v1/auth/login/', data=json.dumps(
            dict(email='admin@gmail.com', password='12345678')),
                                       content_type='application/json')
        return json.loads(res_login.data.decode())["access_token"]

    def test_get_products(self):
        '''Test for  creating a product '''

        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.products), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product created successfully')
        self.assertEqual(response.status_code, 201)

        '''Test  gets all products'''
        response = self.client.get(GET_ALL_PRODUCTS,
                                   headers=dict(Authorization="Bearer " + self.login()),
                                   content_type = 'application/json')   
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product retrieved succesfully')
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        '''Test for  creating a product '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.products), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product created successfully')
        self.assertEqual(response.status_code, 201)


    def test_empty_name_product(self):
        '''Test for ceating empty product name '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.empty_products_name),
                                    headers=dict(Authorization="Bearer " + self.login()), 
                                    content_type = 'application/json')
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product name can not be empty')
        self.assertEqual(response.status_code, 400)


    def test_empty_price_product(self):
        '''Test for empty product price '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.empty_price), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json') 
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'price of product cannot be empty')
        self.assertEqual(response.status_code, 400)


    def test_empty_minimum_product(self):
        '''Test for empty product '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.empty_min_stock), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json') 
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'minimum stock  cannot be empty')
        self.assertEqual(response.status_code, 400)

    def test_empty_quantity_product(self):
        '''Test for empty product '''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.empty_quantity), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json') 
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'quantity of product cannot be empty')
        self.assertEqual(response.status_code, 400)


    def test_get_products(self):
        '''Test Get all products'''
        response = self.client.post(CREATE_PRODUCT_URL,
                                    data = json.dumps(self.products), 
                                    headers=dict(Authorization="Bearer " + self.login()),
                                    content_type = 'application/json')
        self.assertEqual(response.status_code, 201)

        '''Test  gets all products'''
        response = self.client.get(GET_ALL_PRODUCTS,
                                   headers=dict(Authorization="Bearer " + self.login()),
                                   content_type = 'application/json')   
        resp_data = json.loads(response.data.decode())
        self.assertEqual(resp_data['message'], 'product retrieved succesfully')
        self.assertEqual(response.status_code, 200)

        delete_tables()
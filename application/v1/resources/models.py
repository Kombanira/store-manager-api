from flask_restful import Resource,reqparse
from flask import Flask,jsonify,request, make_response


products = []


class Product():

# create a product by admin
        def create_product(name,price,quantity):
            id = len(products) + 1
            new_product = { 'id':id ,'name':name,'price':price,'quantity':quantity}
            products.append(new_product)
            return products

# fetch all products by admin
        def get_products():

            return products


# fetch a single product 
        def get_each_product(product_id):
            product_index= product_id - 1

            return products[product_index]


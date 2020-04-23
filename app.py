# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:33:25 2020

@author: Avijit
"""

#loading necessary libraries
from explore_database import explore_database
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
    
# app
app = Flask(__name__)

query_list11 = [
    "discounted_products_list",
"discounted_products_count|avg_discount",
"expensive_list",
"competition_discount_diff_list"
    ]

#Connecting the database
mongo = PyMongo(app,uri="mongodb://naptest:1234nap@ds135966.mlab.com:35966/heroku_66751cjb")
collection = mongo.db.products


# routes
@app.route("/",methods=['POST'])
def predict():
    
    data = request.get_json(force=True)
    filter_list = data["filters"]
    query = data["query_type"]
    ob = explore_database()
    #print(query)
    #print(filter_list)
    query_response,flag = ob.route_query(filter_list,collection)
    #print(query_response)
    if (query == query_list11[0]):
        response = ob.discounted_products_list(query_response)
    elif (query == query_list11[1]):
        response = ob.discounted_products_count(query_response)
    elif (query == query_list11[2]):
        response = ob.expensive_list(query_response)
    elif (query == query_list11[3]):
        for query in filter_list:
            if (query["operand1"]=="competition"):
                competition_id=query["operand2"]
            elif (query["operand1"]=="discount_diff"):
                discount_diff=query["operand2"]
                op=query["operator"]
        response = ob.competition_discount_diff_list(query_response,competition_id, discount_diff, op)
            

    return jsonify(results=response)

if __name__ == '__main__':
    app.run(port = 5000)




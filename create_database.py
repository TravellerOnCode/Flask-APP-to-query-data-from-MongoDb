# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:11:04 2020

@author: Avijit
"""


from flask_pymongo import pymongo
from bson.json_util import loads
#import json
#import os

#Creating a database and collection
def create_db_collection(db_name,col_name):
    myclient = pymongo.MongoClient("mongodb://naptest:1234nap@ds135966.mlab.com:35966/heroku_66751cjb")
    mydb = myclient[db_name]
    mycol = mydb[col_name]
    
#Compute Discount
def compute_discount(collection):
    d = collection.find()
    for i in d:
        idd = i["_id"]
        rp = (i["price"]["regular_price"]["value"])
        op = (i["price"]["offer_price"]["value"])
        dis = (float)((rp - op)/rp)*100
        collection.update_one({"_id":idd},{"$set":{"discount":dis}})
        
    print('Field Added !')
    
#Loading data to the collection and adding a discount field
def load_data(collection):
    product_json=[]
    with open('netaporter_gb_similar_new.json',encoding='utf-8') as fp:
        for product in fp.readlines():
            #print(type(product))
            #mycol.insert(product)
            #break
            product_json.append(loads(product))
            
    data = product_json
    for doc in data:
        collection.insert_one(doc)
    print('Data Loaded !')    
    #add the discount field
    compute_discount(collection)
    #return (product_json)
    

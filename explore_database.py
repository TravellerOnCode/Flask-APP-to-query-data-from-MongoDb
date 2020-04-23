# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:26:53 2020

@author: Avijit
"""

from flask_pymongo import pymongo

#from flask.ext.pymongo import PyMongo

class explore_database:
        
     #takes a feature and performs > , < , ==
     def query_data(self,operand1,operator,operand2,collection):
         
         filters = {}
         for i in range(len(operator)):
             op1 = operand1[i]
             opr = operator[i]
             op2 = operand2[i]
             d = {opr:op2}
             #creating a dictionary of the filters applicable
             filters[op1] = d
    
        #Querying data from the Database    
         response = collection.find(filters)
         return (response)  
    
     def discounted_products_list(self,cursor):
        list_ID = []
        for i in cursor:
            #store the string value in object ID
            list_ID.append(str(i['_id']))
        response = { "discounted_products_list": list_ID }
        return response
    
    
    #Creating a average discount along with the number of products
     def discounted_products_count(self,cursor):     
        s = f = 0
        for i in cursor:
            s = s + i["discount_value"]
            f = f + 1
        if (f == 0):
            avg_discount = 0
        else:
            avg_discount = (float)(s/f)
        response = { "discounted_products_count": f, "avg_discount": avg_discount }
        return response
    
    
    #Creating a list of products that are expensive
     def expensive_list(self,cursor):
        list_ID = []
        for i in cursor:
            a = i["price"]["basket_price"]["value"]
            c = i["similar_products"]["website_results"]
            k = list(c.keys())
            for j in k:
                if len(c[j]["knn_items"]) != 0:
                    b = c[j]["knn_items"][0]
                    b = b["_source"]["price"]["basket_price"]["value"]
                    if (b <= a):
                        list_ID.append(str(i["_id"]))
                        #print("ID :",i["_id"],"  BP : ",a,"  CBP : ",b)
                    

        response = { "expensive_list": list_ID }
        return response
    
     def discount_difference(self,a,b):
        if (a > b):
            s = a - b
            r = b
        else:
            s = b - a
            r = a
        return (s/r)*100
    
     def compare(self,a,b,op):
        if (op == "=="):
            if (a == b):
                result = True
            else:
                result = False
        elif (op == ">"):
            if (a > b):
                result = True
            else:
                result = False
        elif (op == "<"):
            if (a < b):
                result = True
            else:
                result = False
            
        return result

     """
    Creating a list of competition products
    The parameter details are as follows:
    1. query_data : The Data received after applying filters
    2. competition_id : The Website ID of the competitors website
    3. discount_diff : The desired value of discount difference
    4. op : The operator whether > , == , <
    """

     def competition_discount_diff_list(self,query_data,competition_id,discount_diff,op):
        #r = collection.find()
        list_IDs = []
        for i in query_data:
            a = i["price"]["basket_price"]["value"]
            b = i["similar_products"]["website_results"][competition_id]["knn_items"]
            if (len(b) != 0):
                b = b[0]
                c = b["_source"]["price"]["basket_price"]["value"]
                dis_diff = self.discount_difference(a,c)
                #print ("NAP Product BP :",a ," Competitors BP :" ,c ," + :", dis_diff," Brand_Name - ",i["brand"]["name"], "  D - ",i["discount_value"])
        
                if (self.compare(dis_diff,discount_diff,op)):
                    list_IDs.append(str(i["_id"]))
    
        response = { "competition_discount_diff_list": list_IDs }
        return response
    
    
    
    #call the appropriate to query the database
     def route_query(self, filter_list,collection):
        operand1_list = []
        operator_list = []
        operand2_list = []
        flag = 0 #this is to detect the presence of a hybrid field i.e a field derived from the original fields
        for i in filter_list:
            if i["operand1"] in ['discount_diff','competition']:
                flag = 1
                continue
            operand1_list.append(i["operand1"])
            o = i["operator"]
            if (o == "=="):
                o = "$eq"
            elif (o == ">"):
                o = "$gt"
            elif (o == "<"):
                o = "$lt"
            operator_list.append(o)
            operand2_list.append(i["operand2"])
        
        query_response = self.query_data(operand1_list, operator_list, operand2_list,collection)
        #print (len(response))
        return (query_response,flag)
    
    

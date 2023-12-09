import requests
import time
import sys
import json
from pprint import pprint
import pymongo
from pymongo import MongoClient
from datetime import datetime

get_date=datetime.today()
format_date=datetime.strftime(get_date,'%Y-%m-%d')

def mongo_connection(db,collection):
    global col_conn
    try:
        host="host_name_here"
        time_out=3000
        user="user_name_here"
        pwd="password_here"

        mon_conn = MongoClient(host=host,serverSelectionTimeoutMS=time_out,username=user,password=pwd)
        db_conn = mon_conn[db]
        col_conn= db_conn[collection]
        print("Mongodb connected")
    except Exception as e:
        print("Error in connecting to mongo db",exc_info=True)

url = f"http://127.0.0.1:8080/test/"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

start_time = time.time()
status=response.json()
end_time = time.time() 

get_res_time = end_time - start_time
get_success_status=response.json().get("success")
get_data_len=len(response.json().get("data"))
get_http_status_code=response.status_code

u_date=response.json().get("date")
u_time=response.json().get("time")

print("Response_time",get_res_time)
print("Response Status",get_success_status)
print("Data length",get_data_len)
print("Http Status Code",get_http_status_code)
print("Data length",u_date)
print("Data length",u_time)

def test_Response_status():
    global Response_status
    if response.status_code == 200:
        print("Request was successful")
        Response_status="pass"
        assert True
    else:
        Response_status="fail"
        print("Request failed.")
        assert False

def test_Response_time():
    global Response_time
    if get_res_time <= 3000:
        print(f"Request was successful with a response time of {get_res_time} seconds.")
        Response_time="pass"
        assert True
    else:
        print(f"Response time: {get_res_time}, is more then 3s")
        Response_time="fail"
        assert False

def test_Success_status():
    global Success_status
    if response.json().get("success")==True:
        print("Success status is true")
        Success_status="pass"
    else:
        print("Success failure")
        Success_status="fail"

def test_No_prdts():
    global tot_prdts
    if get_data_len==3:
        tot_prdts="pass"
        print("Product count validated")
    else:
        tot_prdts="fail"
        print("Product count mismatch")



def test_add_mongo():
    test_Response_time()
    test_Success_status()
    test_No_prdts()
    client="dummy_client"
    mongo_connection()
    update_doc={
            
                f"{client}:{u_date}.{u_time}":{
                    
                        "response_time":Response_time,
                        "success_status":Success_status,
                        "total_prdt_count":tot_prdts,
                        "response_status_code":Response_status
                        
                    }
            
        }
    result=col_conn.external_reports_summary.update_one({'_id':format_date},{'$set':update_doc} , upsert = True)
    print("Inserted document ID:", result.upserted_id)

test_add_mongo()
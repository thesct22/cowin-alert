import requests
import json
import datetime
import uuid
from faker import Faker
import time
import random
import os
import sys
import traceback


sys.stdout.flush()

file1 = open("output.txt","a")

faker = Faker()

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
            'origin': 'https://selfregistration.cowin.gov.in',
            'referer': 'https://selfregistration.cowin.gov.in/'
        }
def crawl_cowin(pin_code_list,date):
    ip_addr = faker.ipv4()
    headers["X-Forwarded-For"] = ip_addr
    if date is None:
        date = datetime.datetime.now().strftime("%d-%m-%Y")
    for pin_code in pin_code_list:
        response = requests.get(
            "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+pin_code
            +"&date="+date+"&random="+uuid.uuid4().__str__(),
            verify=False, headers=headers)
        try:
            resp_obj = json.loads(response.content)
            time.sleep(1)
            center_list = resp_obj["centers"]
            time.sleep(1)
            for center in center_list:
                session_list = center["sessions"]
                for session in session_list:
                    available_capacity = session['available_capacity_dose1']
                    min_age_limit = session["min_age_limit"]
                    vaccine = session["vaccine"]
                    if min_age_limit == 18 and vaccine == 'COVISHIELD':
                        print(session)
                        file1 = open("outputtombkp.txt","a")
                        file1.write(str(session))
                        file1.write("\n")
                        file1.write(str(datetime.datetime.now()))
                        file1.write("\n")
                        file1.close()
                    if available_capacity > 0 and min_age_limit == 18:
                        print("Pincode:"+pin_code+" Available capacity :"+str(available_capacity),flush=True)
                        os.system("play song.wav")
                        sys.exit(0)
        except Exception as exp:
            print("Exception is "+str(exp),flush=True)
            os.system("play song.wav")
            traceback.print_exc()
            time.sleep(random.randint(5, 20))

i = 0
pin_codes = ["673004"]
while True:
    print("Iteration count :"+str(i), flush=True)
    crawl_cowin(pin_codes,date="28-05-2021")
    time.sleep(6)
    i+=1

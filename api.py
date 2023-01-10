from fastapi import FastAPI
from uvicorn import run
from faker import Faker
from faker.providers import internet
from faker_vehicle import VehicleProvider
import json
import datetime

api = FastAPI()

key_json = json.loads(open("keys.json", "r").read())
keys = ["r7NIL9CHmqNdNy8jKvDapX-krI2zWNsxcwrSN1WDO2A=", "FJ3LLBnGL-etfp1LE56_lqh2smb7-wpKJhaqMDLSFLs=", "NCfcxQFRLCZMSC0p-vu7feQBX8LShv4_5pbMad3PI2Q="]

@api.get("/key_verify/k={key}")
def verify(key):
    try:
        return key_json[key]
    except:
        return {"error": "key don't exist"}

@api.get("/credits")
def credits():
    return {"creators": "sukilovot ORG SURU"}

@api.get("/generate/c={country},k={key}")
def fakedatas(country, key):
    if key in keys:
        if key == "r7NIL9CHmqNdNy8jKvDapX-krI2zWNsxcwrSN1WDO2A=" and key_json[key]["generateTimes"] > 0:
            key_json[key]['generateTimes'] -= 1

        if key_json[key]['generateTimes'] == "infinite" or key_json[key]['generateTimes'] > 0:
            try:
                fdata = Faker(country)
                fdata.add_provider(internet)
                fdata.add_provider(VehicleProvider)

                data = {
                    "name": fdata.name(),
                    "ssn": fdata.ssn(),
                    "address": fdata.address().replace(" / ", "-"),
                    "ip": fdata.ipv4(),
                    "phoneNumber": fdata.phone_number(),
                    "email": fdata.ascii_free_email(),
                    "job": {
                        "corporationName": fdata.company(),
                        "corporationCatchPhrase": fdata.catch_phrase(),
                        "job": fdata.job(),
                        "companyEmail": fdata.company_email()
                    },
                    "cc": {
                        "number": fdata.credit_card_number(),
                        "provider": fdata.credit_card_provider(),
                        "expire": fdata.credit_card_expire(),
                        "securityCode": fdata.credit_card_security_code()
                    },
                    "bankAccount": {
                        "basic": fdata.bban(),
                        "international": fdata.iban()
                    },
                    "vehicle": {
                        "model": fdata.vehicle_year_make_model_cat(),
                        "licensePlate": fdata.license_plate(),
                        "color": fdata.color()
                    }
                }

                return data
            except Exception as err:
                err_date_and_time = str(datetime.datetime.now())
                return {"error": err, "dateAndTime": err_date_and_time}
        elif key_json[key]['generateTimes'] == 0:
            err_date_and_time = str(datetime.datetime.now())
            return {"error": "time to generate is over", "dateAndTime": err_date_and_time}
    else:
        err_date_and_time = datetime.datetime.now()
        return {"error": "key invalid or country invalid", "dateAndTime": err_date_and_time}

run(api)
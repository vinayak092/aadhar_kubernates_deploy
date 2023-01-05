import argparse
import logging
import pandas as pd
import redis
import requests
import hashlib
import datetime
import json

from sanic import Sanic, response

from bot_responses import generate_response

logger = logging.getLogger(__name__)

DEFAULT_SERVER_PORT = 7114

DEFAULT_SANIC_WORKERS = 100

REDIS_HOST = "my-release-redis-master.default.svc.cluster.local"
REDIS_PORT = 6379
REDIS_DB = 10
REDIS_DB_1 = 5
REDIS_PASSWORD = "9CcVSjiGPD"
REDIS_DB_CONV = "0"
red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD,charset="utf-8", decode_responses=True)
red_customers = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_1, password=REDIS_PASSWORD,charset="utf-8", decode_responses=True)

def create_argument_parser():
    """Parse all the command line arguments for the nlg server script."""

    parser = argparse.ArgumentParser(description="starts the nlg endpoint")
    parser.add_argument(
        "-p",
        "--port",
        default=DEFAULT_SERVER_PORT,
        type=int,
        help="port to run the server at",
    )
    parser.add_argument(
        "--workers",
        default=DEFAULT_SANIC_WORKERS,
        type=int,
        help="Number of processes to spin up",
    )

    return parser

mapped_languages={
    "english":"en",
    "hindi":"hi",
    "tamil":"tam",
    "telugu":"tel",
    "kannada":"ka",
    "malayalam":"ml",
    "marathi":"ma",
    "punjabi":"pa",
    "bangla":"bn",
    "gujarati":"gu"
}

def detect_language_from_redis(data):
    user_id=data['user_id']
    data=red_customers.hgetall(user_id)
    print("data",data)
    lang = data.get("language").lower()
    return mapped_languages[lang]

def maintain_bot_log(request=None,response=None,session_id=None,in_time=None,out_time=None):
    delay = out_time-in_time
    with open("bot_response_log.txt","a") as f:
        f.write("session_id -----> %s"%session_id+"\t"+"request-----> %s"%request+"\t"+"response------> %s"%response+"\t"+"intime------> %s"%in_time+"\t"+"out_time------> %s"%out_time+"\t"+"delay------> %s"%delay+"\n")


def detect_language(data):
    user_id=data['user_id']
    with open("customer_details.json", "r+", encoding='utf-8') as f:
        customer_details = json.load(f)
    for customer in customer_details:
        if int(customer['phone_number'])==int(user_id):
            return customer["custom_field_2"]
    user_id="9851197922"
    for customer in customer_details:
        if int(customer['phone_number'])==user_id:
            return customer["custom_field_2"]
    return "hi"


def run_server(port, workers):
    app = Sanic(__name__)

    @app.route("/webhook", methods=["POST", "OPTIONS"])
    async def nlg(request):
        in_time = datetime.datetime.now()
        nlg_call = request.json
        print(nlg_call)
        nlu_data = nlg_call.get("nlu_data", None)
        sender_id = nlg_call.get("sender",None)
        print("sender_id",sender_id)
        print("nlu_data",nlu_data)
        if nlu_data is None:
            print("Inside the nlu_data is None:",nlu_data)
            red.hset("cz","5","yes")
            red.hset("backend","5","no")
        else:
            red.hset("cz","5","no")
            red.hset("backend","5","yes")
        data=red.hget("cz","5")
        print("data",data)
        if data == "yes":
            print("inside yes")
            language=detect_language(nlg_call)
        else:
            print("inside no")
            language=detect_language_from_redis(nlg_call)
        print("Language:",language)
        try:
            nlg_call = request.json
            print("NLG data:",nlg_call)
            if language.lower()=="en":
                bot_response = await generate_response(nlg_call)
            elif language.lower()=="hi":
                print("coming here for language cheange..........")
                bot_response=requests.post("http://localhost:8001/webhook",json=nlg_call).json()
            # elif language.lower()=="tam":
            #     bot_response=requests.post("http://adhar.saarthi.ai/aadhar_tamil/webhook",json=nlg_call).json()
            # elif language.lower()=="tel":
            #     bot_response=requests.post("http://adhar.saarthi.ai/aadhar_telugu/webhook",json=nlg_call).json()
            # elif language.lower() == "ka":
            #     bot_response=requests.post("http://adhar.saarthi.ai/aadhar_kannada/webhook",json=nlg_call).json()
            # elif language.lower() == "ml":
            #     bot_response=requests.post("https://adhar.saarthi.ai/aadhar_malayalam/webhook",json=nlg_call).json() 
            endtime = datetime.datetime.now() 
            maintain_bot_log(request=nlg_call,session_id=sender_id,response=bot_response,in_time=in_time,out_time=endtime)
            return response.json(bot_response)
        except:
            logging.error("Error Message")
        # return response.json(bot_response)

    app.run(host="0.0.0.0", port=port, workers=workers)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Running as standalone python application
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    run_server(cmdline_args.port, cmdline_args.workers)

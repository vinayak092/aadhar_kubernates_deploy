import hashlib
import logging
import time
import datetime
import redis
import requests
import os

from orchestrator_check import store_call_bot_output

logger = logging.getLogger(__name__)
REDIS_HOST = "my-release-redis-master.default.svc.cluster.local"
REDIS_PORT = 6379
REDIS_DB_ENGLISH = 1
REDIS_DB_HINDI = 2
REDIS_DB_KANNADA=3
REDIS_DB_TELUGU=4
REDIS_DB_TAMIL=5
REDIS_DB_MALAYALAM=6
REDIS_DB_1=5
REDIS_DB = 10
REDIS_PASSWORD = "9CcVSjiGPD"
REDIS_DB_CONV = "0"
red_english = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_ENGLISH, password=REDIS_PASSWORD)
red_hindi = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_HINDI, password=REDIS_PASSWORD)
red_telugu = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_TELUGU, password=REDIS_PASSWORD)
red_kannada = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_KANNADA, password=REDIS_PASSWORD)
red_tamil = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_TAMIL, password=REDIS_PASSWORD)
# red_bengali = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_BENGALI, password=REDIS_PASSWORD)
red_malayalam = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_MALAYALAM, password=REDIS_PASSWORD)
# red_punjabi = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_PUNJABI, password=REDIS_PASSWORD)
# red_marathi = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_MARATHI, password=REDIS_PASSWORD)
red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD,charset="utf-8", decode_responses=True)
red_customers = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_1, password=REDIS_PASSWORD,charset="utf-8", decode_responses=True)

audio_url = os.environ.get('audio_url')
if audio_url is None:
    audio_url = "https://adhar.saarthi.ai/aadhar_tts"

async def call_bot(url, sender_id, request_id, user_id, text):
    """Call to the bot Api"""

    bot_response = {
        "sender_id": "",
        "request_id": "",
        "user_id": "",
        "nlu_data": {
            "entities": [],
            "intent": {
                "confidence": 1,
                "name": "greet"
            },
            "intent_ranking": [],
            "text": ""
        },
        "custom": {
            "status": 701
        },
        "data": [
            {
                "text": "<speak>Server is Down. Please try after sometime</speak>",
                "buttons": [],
                "quick_replies": [],
                "hash": str(
                    hashlib.md5("<speak>Server is Down. Please try after sometime</speak>".encode('utf-8')).hexdigest())
            }
        ],
        "elements": [],
        "attachments": []
    }
    response = dict()
    try:
        response = requests.post(url, json={"sender": sender_id, "request_id": request_id, "user_id": user_id,
                                            "message": str(text)}).json()
        return response


    except requests.exceptions.HTTPError as errh:
        logger.exception("Http Error: {}".format(errh))
        return bot_response
    except requests.exceptions.ConnectionError as errc:
        logger.exception("HError Connecting: {}".format(errc))
        return bot_response
    except requests.exceptions.Timeout as errt:
        logger.exception("Timeout Error: {}".format(errt))
        return bot_response
    except requests.exceptions.RequestException as err:
        logger.exception("Error: {}".format(err))
        return bot_response

    return response


async def generate_response(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    # print("ENGLISH NLG:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)
    print("***************The input message",text)
    if text == "/pre_emi" or text == "/post_emi" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if text:
        text = text.lower()

    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response

    
    data = red.hget("cz","5")
    if data == "no":
        # print("text----------->",text)
        if text != "/initial_message":
            if text != "/no_message":
                nlu = nlg_call.get("nlu_data", None)
                ner = nlg_call.get("ner_data",None)
                if ner is not None and ner !="":
                    text = text +" "+"<nlu>"+str(nlu)+"<ner>"+str(ner)
                else:
                    text = text +" "+"<nlu>"+str(nlu)
        
    session_value_hindi_old = red_english.get(str(sender_id)+"hindi")
    # session_value_kannada_old = red_english.get(str(sender_id)+"kannada")

    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        bot_responses = await generate_response_hindi(nlg_call)
        red_english.set(str(sender_id)+"hindi", "True", ex=300)
        return bot_responses
    # if session_value_telugu_old is not None and str(session_value_telugu_old, 'utf-8') == "True":
    #     bot_responses = await generate_response_telugu(nlg_call)
    #     red_english.set(str(sender_id)+"telugu", "True", ex=300)
    #     return bot_responses
    # elif session_value_kannada_old is not None and str(session_value_kannada_old, 'utf-8') == "True":
    #     bot_responses = await generate_response_kannada(nlg_call)
    #     red_english.set(str(sender_id)+"kannada", "True", ex=300)
    #     return bot_responses
    # if session_value_malayalam_old is not None and str(session_value_malayalam_old, 'utf-8') == "True":
    #     bot_responses = await generate_response_malayalam(nlg_call)
    #     red_english.set(str(sender_id)+"malayalam", "True", ex=300)
    #     return bot_responses
    # if session_value_tamil_old is not None and str(session_value_tamil_old, 'utf-8') == "True":
    #     bot_responses = await generate_response_tamil(nlg_call)
    #     red_english.set(str(sender_id)+"tamil", "True", ex=300)
    #     return bot_responses
    # if session_value_bengali_old is not None and str(session_value_bengali_old, 'utf-8') == "True":
    #     bot_responses = await generate_response_bengali(nlg_call)
    #     red_english.set(str(sender_id)+"bengali", "True", ex=300)
    #     return bot_responses
    # if session_value_marathi_old is not None and str(session_value_marathi_old, 'utf-8') == "True":
    #     bot_responses = await generate_response_marathi(nlg_call)
    #     red_english.set(str(sender_id)+"marathi", "True", ex=300)
    #     return bot_responses
    # if session_value_punjabi_old is not None and str(session_value_punjabi_old, 'utf-8') == "True":
    #     bot_responses = await generate_response_punjabi(nlg_call)
    #     red_english.set(str(sender_id)+"punjabi", "True", ex=300)
    #     return bot_responses

    if "hindi" in text:

        red_english.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"english","False",ex= 300)
        bot_responses = await generate_response_hindi(nlg_call)
        return bot_responses
    # if "kannada" in text:
    #     # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     # print(intent)
    #     # intent = intent["label"][0]["name"]
    #     # if intent == "language_change":
    #     red_english.set(str(sender_id)+"kannada", "True", ex=300)
    #     red_kannada.set(str(sender_id)+"english","False",ex = 300)
    #     bot_responses = await generate_response_kannada(nlg_call)
    #     return bot_responses
    # if "telugu" in text:
    #     # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     # print(intent)
    #     # intent = intent["label"][0]["name"]
    #     # if intent == "language_change":
    #     red_english.set(str(sender_id)+"telugu", "True", ex=300)
    #     red_telugu.set(str(sender_id)+"english","False",ex = 300)
    #     bot_responses = await generate_response_telugu(nlg_call)
    #     return bot_responses
    # if "tamil" in text:
    #     # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     # print(intent)
    #     # intent = intent["label"][0]["name"]
    #     # if intent == "language_change":
    #     red_english.set(str(sender_id)+"tamil", "True", ex=300)
    #     red_tamil.set(str(sender_id)+"english","False",ex = 300)
    #     bot_responses = await generate_response_tamil(nlg_call)
    #     return bot_responses
    # if "malayalam" in text:
    #     # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     # print(intent)
    #     # intent = intent["label"][0]["name"]
    #     # if intent == "language_change":
    #     red_english.set(str(sender_id)+"malayalam", "True", ex=300)
    #     red_malayalam.set(str(sender_id)+"english","False",ex = 300)
    #     bot_responses = await generate_response_malayalam(nlg_call)
    #     return bot_responses
    # if "punjabi" in text:
    #     # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     # print(intent)
    #     # intent = intent["label"][0]["name"]
    #     # if intent == "language_change":
    #     red_english.set(str(sender_id)+"punjabi", "True", ex=300)
    #     red_punjabi.set(str(sender_id)+"english","False",ex = 300)
    #     bot_responses = await generate_response_punjabi(nlg_call)
    #     return bot_responses
    # if "marathi" in text:
    #     # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     # print(intent)
    #     # intent = intent["label"][0]["name"]
    #     # if intent == "language_change":
    #     red_english.set(str(sender_id)+"marathi", "True", ex=300)
    #     red_marathi.set(str(sender_id)+"english","False",ex = 300)
    #     bot_responses = await generate_response_marathi(nlg_call)
    #     return bot_responses
    # if "bengali" in text or "bangla" in text:
    #     # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     # print(intent)
    #     # intent = intent["label"][0]["name"]
    #     # if intent == "language_change":
    #     red_english.set(str(sender_id)+"bengali", "True", ex=300)
    #     red_bengali.set(str(sender_id)+"english","False",ex = 300)
    #     bot_responses = await generate_response_bengali(nlg_call)
    #     return bot_responses

    # url = "http://20.127.208.146/core_english/webhooks/rest/webhook"
    url = "http://localhost:8650/webhooks/rest/webhook"
    # url = "http://adhar.saarthi.ai/aadhar_english_core/webhooks/rest/webhook"

    bot_response = await call_bot(url, sender_id, request_id, user_id, text)
    print("ENTERING HERE >>>>>>>>>>>>>")

    if bot_response.get("custom", None) is None:
        bot_response["custom"] = {}
    bot_response["custom"]["tts"] = "en-IN"
    bot_response["custom"]["stt"] = "en-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "en-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8
    print("ENTERING HERE <<<<<<<<")
    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    print("bot_utterances>>>>.",bot_utterances)
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template_name>")[0]
        template_name=item["text"].split("<template_name>")[1]
        item['text']=item["text"].split("<template_name>")[0]
        hash_object = hashlib.md5((message+"abc").encode('utf-8'))
        file_name = str(hash_object.hexdigest())
        item['hash'] = file_name
        if text == "/no_message":
            item['force']=1
        elif text == "/initial_message":
            item['force']=1
        elif text == "/deny":
            item['force']=0
        else:
            item['force']=0
        item[
            "voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language=" \
                            "{language}".format(message=message, template_name=template_name, language="english",audio_url=audio_url)
        # item["voice_data"] = "https://navidockertest.blob.core.windows.net/availfinanceresponses/{}.wav".format(
        #     file_name)
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses

    return bot_response


async def generate_response_hindi(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    # print("Hindi NLG:",nlg_call)
    print("calling hindi function")
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)
    if text == "/pre_emi" or text == "/post_emi" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if text:
        text = text.lower()

    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response

    data = red.hget("cz","5")
    if data == "no":
        print("text is ------>",text)
        if text != "/initial_message":
            if text != "/no_message":
                nlu = nlg_call.get("nlu_data", None)
                ner = nlg_call.get("ner_data",None)
                if ner is not None and ner !="":
                    text = text +" "+"<nlu>"+str(nlu)+"<ner>"+str(ner)
                else:
                    text = text +" "+"<nlu>"+str(nlu)

    session_value_english_old = red_hindi.get(str(sender_id)+"english")
    session_value_kannada_old = red_hindi.get(str(sender_id)+"kannada")
    print("session_value_english_old-----",session_value_english_old)

    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        bot_responses = await generate_response(nlg_call)
        red_hindi.set(str(sender_id)+"english", "True", ex=300)
        return bot_responses
    elif session_value_kannada_old is not None and str(session_value_kannada_old, 'utf-8') == "True":
        bot_responses = await generate_response_kannada(nlg_call)
        red_hindi.set(str(sender_id)+"kannada", "True", ex=300)
        return bot_responses

    # if "अंग्रेजी" in text or "इंग्लिश" in text or "english" in text or "English" in text or "अंग्रेज़ी" in text  or "अंग्रेज" in text:
    if "अंग्रेजी" in text or "इंग्लिश" in text or "अंग्रेज़ी" in text  or "अंग्रेज" in text:

        red_hindi.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"hindi","False",ex = 300)
        bot_responses = await generate_response(nlg_call)
        return bot_responses

    # if "कनाडा" in text or "कन्नड़" in text:
    #     # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     # print(intent)
    #     # intent = intent["label"][0]["name"]
    #     # session_value_kannada = red_kannada.get(str(sender_id)+"kannada")
    #     # if intent == "language_change":
    # #         # if session_value_kannada is not None and str(session_value_kannada, 'utf-8') == "True":
    # #         #     text = "/language_change"
    # #         # else:
    # #         # nlg_call["message"] = "/change_language_from_hindi_to_kannada"
    #     red_hindi.set(str(sender_id)+"kannada", "True", ex=300)
    #     red_kannada.set(str(sender_id)+"hindi","False",ex = 300)
    #     bot_responses = await generate_response_kannada(nlg_call)
    #     return bot_responses
    # if "तमिल" in text:
    # #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    # #     print(intent)
    # #     intent = intent["label"][0]["name"]
    # #     if intent == "language_change":
    #     red_hindi.set(str(sender_id)+"tamil", "True", ex=300)
    #     red_tamil.set(str(sender_id)+"hindi","False",ex = 300)
    #     bot_responses = await generate_response_tamil(nlg_call)
    #     return bot_responses
    # if "तेलुगू" in text:
    # #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    # #     print(intent)
    # #     intent = intent["label"][0]["name"]
    # #     if intent == "language_change":
    #     red_hindi.set(str(sender_id)+"telugu", "True", ex=300)
    #     red_telugu.set(str(sender_id)+"hindi","False",ex=300)
    #     bot_responses = await generate_response_telugu(nlg_call)
    #     return bot_responses
    # # if "बंगाली" in text or "बांग्ला" in text:
    # #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    # #     print(intent)
    # #     intent = intent["label"][0]["name"]
    # #     if intent == "language_change":
    # #         red_hindi.set(str(sender_id)+"bengali", "True", ex=300)
    # #         red_bengali.set(str(sender_id)+"hindi","False",ex=300)
    # #         bot_responses = await generate_response_bengali(nlg_call)
    # #         return bot_responses
    # if "मलयालम" in text:
    # #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    # #     print(intent)
    # #     intent = intent["label"][0]["name"]
    # #     if intent == "language_change":
    #     red_hindi.set(str(sender_id)+"malayalam", "True", ex=300)
    #     red_malayalam.set(str(sender_id)+"hindi","False",ex=300)
    #     bot_responses = await generate_response_malayalam(nlg_call)
    #     return bot_responses
    # if "मराठी" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_hindi.set(str(sender_id)+"marathi", "True", ex=300)
    #         red_marathi.set(str(sender_id)+"hindi","False",ex=300)
    #         bot_responses = await generate_response_marathi(nlg_call)
    #         return bot_responses

    # if "पंजाबी" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_hindi.set(str(sender_id)+"punjabi", "True", ex=300)
    #         red_punjabi.set(str(sender_id)+"hindi","False",ex=300)
    #         bot_responses = await generate_response_punjabi(nlg_call)
    #         return bot_responses
    url = "http://localhost:8550/webhooks/rest/webhook"
    # url = "http://adhar.saarthi.ai/aadhar_hindi_core/webhooks/rest/webhook"
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)

    if bot_response.get("custom", None) is None:
        bot_response["custom"] = {}
    bot_response["custom"]["tts"] = "hi-IN"
    bot_response["custom"]["stt"] = "hi-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "hi-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template_name>")[0]
        template_name=item["text"].split("<template_name>")[1]
        item['text']=item["text"].split("<template_name>")[0]
        hash_object = hashlib.md5((message+"efc").encode('utf-8'))
        file_name = str(hash_object.hexdigest())
        item['hash'] = file_name
        if text == "/no_message":
            item['force']=1
        elif text == "/initial_message":
            item['force']=1
        else:
            item['force']=0
        item[
            "voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language=" \
                            "{language}".format(message=message, template_name=template_name, language="hindi",audio_url=audio_url)
        # item["voice_data"] = "https://navidockertest.blob.core.windows.net/availfinanceresponses/{}.wav".format(
        #     file_name)
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses

    return bot_response


async def generate_response_kannada(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    print("Kannada NLG call:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)

    if text:
        text = text.lower()
    # if text == "/pre_emi" or text == "/post_emi"or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
    #     text = "/initial_message"
    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response

    data=red.hget("cz",sender_id)
    print("data in side generate response",data)
    if data == "no":
        nlu = nlg_call.get("nlu_data", None)
        if nlu['label'][0]['name']!="language_change":
            ner = nlg_call.get("ner_data", None)
            print("nlu",nlu)
            print("ner",ner)
            text="/"+nlu['label'][0]['name']
            print("Tyhe nLu data",text)
            if ner is not None:
                for row in ner:
                    if row["entity"] == "date":
                        try:
                            formatted_date = datetime.datetime.strptime(row["value"], "%d/%m/%Y")
                        except ValueError:
                            formatted_date = datetime.datetime.strptime(row["value"], "%d/%m/%y")
                        date_value = formatted_date.strftime("%d/%m/%y")
                        row["value"] = formatted_date.strftime("%d/%m/%y")
                    text+="{"+"\""+row['entity']+"\":\""+row['value']+"\"}"
    print("text",text)

    session_value_english_old = red_kannada.get(str(sender_id)+"english")
    session_value_hindi_old = red_kannada.get(str(sender_id)+"hindi")

    print("Hindi old:",session_value_hindi_old)
    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response(nlg_call)
        red_kannada.set(str(sender_id)+"english", "True", ex=300)
        return bot_responses
    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_hindi(nlg_call)
        red_kannada.set(str(sender_id)+"hindi", "True", ex=300)
        return bot_responses

    if "ಆಂಗ್ಲ" in text or "ಇಂಗ್ಲಿಷ್" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # session_value_hindi = red_hindi.get(str(sender_id)+"hindi")
        # if intent == "language_change":
            # if session_value_hindi is not None and str(session_value_hindi, 'utf-8') == "True":
            #     text = "/language_change"
            # else:
            # nlg_call["message"] = "/change_language_from_kannada_to_english"
        red_kannada.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"kannada","False",ex = 300)
        bot_responses = await generate_response(nlg_call)
        return bot_responses
    if "ಹಿಂದಿ" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"hindi")
        # if intent == "language_change":
            # if session_value_hindi is not None and str(session_value_hindi, 'utf-8') == "True":
            #     text = "/language_change"
            # else:
            # nlg_call["message"] = "/change_language_from_kannada_to_hindi"
        red_kannada.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"kannada","False",ex = 300)
        bot_responses = await generate_response_hindi(nlg_call)
        return bot_responses
    if "ತಮಿಳು" in text or "ತಮಿಳ್" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_tamil = red_tamil.get(str(sender_id)+"tamil")
        # if intent == "language_change":
        red_kannada.set(str(sender_id)+"tamil", "True", ex=300)
        red_tamil.set(str(sender_id)+"kannada","False",ex = 300)
        bot_responses = await generate_response_tamil(nlg_call)
        return bot_responses
    if "ತೆಲುಗು" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # if intent == "language_change":
        red_kannada.set(str(sender_id)+"telugu", "True", ex=300)
        red_telugu.set(str(sender_id)+"kannada","False", ex=300)
        bot_responses = await generate_response_telugu(nlg_call)
        return bot_responses
    if "ಮಲಯಾಳಂ" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # if intent == "language_change":
        red_kannada.set(str(sender_id)+"malayalam", "True", ex=300)
        red_malayalam.set(str(sender_id)+"kannada","False",ex=300)
        bot_responses = await generate_response_malayalam(nlg_call)
        return bot_responses
    # if "ಬೆಂಗಾಲಿ" in text or "ಬಾಂಗ್ಲಾ" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_kannada.set(str(sender_id)+"bengali", "True", ex=300)
    #         red_bengali.set(str(sender_id)+"kannada","False",ex=300)
    #         bot_responses = await generate_response_bengali(nlg_call)
    #         return bot_responses
    # if "ಮರಾಠಿ" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_kannada.set(str(sender_id)+"marathi", "True", ex=300)
    #         red_marathi.set(str(sender_id)+"kannada","False",ex=300)
    #         bot_responses = await generate_response_marathi(nlg_call)
    #         return bot_responses
    
    print("Entrypoint")
    # url = "http://localhost:8036/webhooks/rest/webhook"
    url = "http://20.127.208.146/core_kannada/webhooks/rest/webhook"
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)

    # if bot_response.get("custom", None) is not None and "language_change" in bot_response.get("custom", None) and \
    #         bot_response.get("custom").get("language_change") is True:
    #     nlg_call["message"] = "/change_language_from_kannada_to_english"
    #     bot_responses = await generate_response(nlg_call)
    #     if session_value_english:
    #         red_english.set(str(sender_id)+"english", "None", ex=300)
    #     red_hindi.set(str(sender_id)+"english", "True", ex=300)
    #     return bot_responses
    if bot_response.get("custom", None) is None:
        bot_response["custom"] = {}
    bot_response["custom"]["tts"] = "kn-IN"
    bot_response["custom"]["stt"] = "kn-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "kn-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template_name>")[0]
        template_name=item["text"].split("<template_name>")[1]
        item['text']=item["text"].split("<template_name>")[0]
        hash_object = hashlib.md5(message.encode('utf-8'))
        file_name = str(hash_object.hexdigest())
        item['hash'] = file_name
        item['force']=0
        item[
            "voice_data"] = "http://adhar.saarthi.ai/aadhar_tts/wav?message={message}&template_name={template_name}&language=" \
                            "{language}".format(message=message, template_name=template_name, language="kannada")
        # item["voice_data"] = "https://navidockertest.blob.core.windows.net/availfinanceresponses/{}.wav".format(
        #     file_name)
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses

    return bot_response

async def generate_response_tamil(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    print("Tamil NLG call:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)

    if text:
        text = text.lower()
    if text == "/pre_emi" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response

    data = red.hget("cz","5")
    if data == "no":
        if text != "/initial_message":
            nlu = nlg_call.get("nlu_data", None)
            ner = nlg_call.get("ner_data",None)
            if ner is not None and ner !="":
                text = text +" "+"<nlu>"+str(nlu)+"<ner>"+str(ner)
            else:
                text = text +" "+"<nlu>"+str(nlu)
    session_value_english_old = red_tamil.get(str(sender_id)+"english")
    session_value_kannada_old = red_tamil.get(str(sender_id)+"kannada")
    session_value_hindi_old = red_tamil.get(str(sender_id)+"hindi")
    session_value_telugu_old =red_tamil.get(str(sender_id)+"telugu")
    session_value_malayalam_old = red_tamil.get(str(sender_id)+"malayalam")

    print("Tamil NLG old:",session_value_hindi_old)
    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response(nlg_call)
        red_tamil.set(str(sender_id)+"english", "True", ex=300)
        return bot_responses
    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_hindi(nlg_call)
        red_tamil.set(str(sender_id)+"hindi", "True", ex=300)
        return bot_responses
    if session_value_kannada_old is not None and str(session_value_kannada_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_kannada(nlg_call)
        red_tamil.set(str(sender_id)+"kannada", "True", ex=300)
        return bot_responses
    if session_value_telugu_old is not None and str(session_value_telugu_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_telugu(nlg_call)
        red_tamil.set(str(sender_id)+"telugu", "True", ex=300)
        return bot_responses
    # if session_value_marathi_old is not None and str(session_value_marathi_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_marathi(nlg_call)
    #     red_tamil.set(str(sender_id)+"marathi", "True", ex=300)
    #     return bot_responses
    # if session_value_bengali_old is not None and str(session_value_bengali_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_bengali(nlg_call)
    #     red_tamil.set(str(sender_id)+"bengali", "True", ex=300)
    #     return bot_responses
    if session_value_malayalam_old is not None and str(session_value_malayalam_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_malayalam(nlg_call)
        red_tamil.set(str(sender_id)+"malayalam", "True", ex=300)
        return bot_responses
    # if session_value_punjabi_old is not None and str(session_value_punjabi_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_punjabi(nlg_call)
    #     red_tamil.set(str(sender_id)+"punjabi", "True", ex=300)
    #     return bot_responses
    # if session_value_gujarati_old is not None and str(session_value_gujarati_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_gujarati(nlg_call)
    #     red_tamil.set(str(sender_id)+"gujarati", "True", ex=300)
    #     return bot_responses

    if "ஆங்கிலம்" in text or "இங்கிலீஷ்" in text or "ஆங்கிலத்தில்" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"hindi")
        # if intent == "language_change":
        red_tamil.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"tamil","False",ex = 300)
        bot_responses = await generate_response(nlg_call)
        return bot_responses
    if "ஹிந்தி" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"hindi")x
        # if intent == "language_change":
        red_tamil.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"tamil","False",ex = 300)
        bot_responses = await generate_response_hindi(nlg_call)
        return bot_responses
    if "கன்னடம்" in text or "கன்னடா" in text or "கன்னட" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
        # if intent == "language_change":
        red_tamil.set(str(sender_id)+"kannada", "True", ex=300)
        red_kannada.set(str(sender_id)+"tamil","False",ex = 300)
        bot_responses = await generate_response_kannada(nlg_call)
        return bot_responses
    if "தெலுங்கு" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
        # if intent == "language_change":
        red_tamil.set(str(sender_id)+"telugu", "True", ex=300)
        red_telugu.set(str(sender_id)+"tamil","False",ex=300)
        bot_responses = await generate_response_telugu(nlg_call)
        return bot_responses

    # if "மராத்தி" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
    #     if intent == "language_change":
    #         red_tamil.set(str(sender_id)+"marathi", "True", ex=300)
    #         red_marathi.set(str(sender_id)+"tamil","False",ex=300)
    #         bot_responses = await generate_response_marathi(nlg_call)
    #         return bot_responses

    # if "பெங்காலி" in text or "பங்கிலா" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
    #     if intent == "language_change":
    #         red_tamil.set(str(sender_id)+"bengali", "True", ex=300)
    #         red_bengali.set(str(sender_id)+"tamil","False",ex=300)
    #         bot_responses = await generate_response_bengali(nlg_call)
    #         return bot_responses

    if "மலையாளம்" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
        # if intent == "language_change":
        red_tamil.set(str(sender_id)+"malayalam", "True", ex=300)
        red_malayalam.set(str(sender_id)+"tamil","False",ex=300)
        bot_responses = await generate_response_malayalam(nlg_call)
        return bot_responses

    # if "பஞ்சாபி" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_tamil.set(str(sender_id)+"punjabi", "True", ex=300)
    #         red_punjabi.set(str(sender_id)+"tamil","False",ex=300)
    #         bot_responses = await generate_response_punjabi(nlg_call)
    #         return bot_responses
    # if "குஜராத்தி" in text or "குஜராத்" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_tamil.set(str(sender_id)+"gujarati", "True", ex=300)
    #         red_gujarati.set(str(sender_id)+"tamil","False",ex=300)
    #         bot_responses = await generate_response_gujarati(nlg_call)
    #         return bot_responses

    # url = "http://localhost:8816/webhooks/rest/webhook"
    # url = "http://localhost:8858/webhooks/rest/webhook"
    url = "http://localhost:8858/webhooks/rest/webhook"


    bot_response = await call_bot(url, sender_id, request_id, user_id, text)


    if bot_response.get("custom", None) is None:
        bot_response["custom"] = {}
    bot_response["custom"]["tts"] = "ta-IN"
    bot_response["custom"]["stt"] = "ta-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "ta-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template_name>")[0]
        template_name=item["text"].split("<template_name>")[1]
        item['text']=item["text"].split("<template_name>")[0]
        hash_object = hashlib.md5(message.encode('utf-8'))
        file_name = str(hash_object.hexdigest())
        item['force']=1
        item[
            "voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language=" \
                             "{language}".format(message=message, template_name=template_name, language="tamil",audio_url=audio_url)
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses

    return bot_response

async def generate_response_telugu(nlg_call):                           
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    print("Telugu NLG call:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)

    if text:
        text = text.lower()
    if text == "/pre_emi" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response

    data=red.hget("cz",sender_id)
    print("data in side generate response",data)
    if data == "no":
        nlu = nlg_call.get("nlu_data", None)
        if nlu['label'][0]['name']!="language_change":
            ner = nlg_call.get("ner_data", None)
            print("nlu",nlu)
            print("ner",ner)
            text="/"+nlu['label'][0]['name']
            print("Tyhe nLu data",text)
            if ner is not None:
                for row in ner:
                    if row["entity"] == "date":
                        try:
                            formatted_date = datetime.datetime.strptime(row["value"], "%d/%m/%Y")
                        except ValueError:
                            formatted_date = datetime.datetime.strptime(row["value"], "%d/%m/%y")
                        date_value = formatted_date.strftime("%d/%m/%y")
                        row["value"] = formatted_date.strftime("%d/%m/%y")
                    text+="{"+"\""+row['entity']+"\":\""+row['value']+"\"}"
    print("text",text)
    session_value_kannada_old = red_telugu.get(str(sender_id)+"kannada")
    session_value_hindi_old = red_telugu.get(str(sender_id)+"hindi")
    session_value_tamil_old=red_telugu.get(str(sender_id)+"tamil")
    session_value_english_old=red_telugu.get(str(sender_id)+"english")
    # session_value_marathi_old = red_telugu.get(str(sender_id)+"marathi")
    # session_value_bengali_old = red_telugu.get(str(sender_id)+"bengali")
    session_value_malayalam_old = red_telugu.get(str(sender_id)+"malayalam")
    # session_value_punjabi_old = red_telugu.get(str(sender_id)+"punjabi")
    # session_value_gujarati_old = red_telugu.get(str(sender_id)+"gujarati")
    
    print("Telugu old:",session_value_hindi_old)
    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_hindi(nlg_call)
        red_telugu.set(str(sender_id)+"hindi", "True", ex=300)
        return bot_responses
    if session_value_kannada_old is not None and str(session_value_kannada_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_kannada(nlg_call)
        red_telugu.set(str(sender_id)+"kannada", "True", ex=300)
        return bot_responses
    if session_value_tamil_old is not None and str(session_value_tamil_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_tamil(nlg_call)
        red_telugu.set(str(sender_id)+"tamil", "True", ex=300)
        return bot_responses
    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response(nlg_call)
        red_telugu.set(str(sender_id)+"english", "True", ex=300)
        return bot_responses
    # if session_value_marathi_old is not None and str(session_value_marathi_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_marathi(nlg_call)
    #     red_telugu.set(str(sender_id)+"marathi", "True", ex=300)
    #     return bot_responses
    # if session_value_bengali_old is not None and str(session_value_bengali_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_bengali(nlg_call)
    #     red_telugu.set(str(sender_id)+"bengali", "True", ex=300)
    #     return bot_responses
    if session_value_malayalam_old is not None and str(session_value_malayalam_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_malayalam(nlg_call)
        red_telugu.set(str(sender_id)+"malayalam", "True", ex=300)
        return bot_responses
    # if session_value_punjabi_old is not None and str(session_value_punjabi_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_punjabi(nlg_call)
    #     red_telugu.set(str(sender_id)+"punjabi", "True", ex=300)
    #     return bot_responses
    # if session_value_gujarati_old is not None and str(session_value_gujarati_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_gujarati(nlg_call)
    #     red_telugu.set(str(sender_id)+"gujarati", "True", ex=300)
    #     return bot_responses


    if "హిందీ" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"hindi")
        # if intent == "language_change":
            # if session_value_hindi is not None and str(session_value_hindi, 'utf-8') == "True":
            #     text = "/language_change"
            # else:
            # nlg_call["message"] = "/change_language_from_kannada_to_hindi"
        red_telugu.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"telugu","False",ex=300)
        bot_responses = await generate_response_hindi(nlg_call)
        return bot_responses
    if "కన్నడ" in text or "కనడ" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
        # if intent == "language_change":
        red_telugu.set(str(sender_id)+"kannada", "True", ex=300)
        red_kannada.set(str(sender_id)+"telugu","False",ex=300)
        bot_responses = await generate_response_kannada(nlg_call)
        return bot_responses
    
    if "తమిళం" in text or "తమిళ్" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
        # if intent == "language_change":
            # if session_value_hindi is not None and str(session_value_hindi, 'utf-8') == "True":
            #     text = "/language_change"
            # else:
            # nlg_call["message"] = "/change_language_from_kannada_to_hindi"
        red_telugu.set(str(sender_id)+"tamil", "True", ex=300)
        red_tamil.set(str(sender_id)+"telugu","False",ex=300)
        bot_responses = await generate_response_tamil(nlg_call)
        return bot_responses
    if "ఆంగ్ల" in text or "ఇంగ్లీష్" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
        # if intent == "language_change":
            # if session_value_hindi is not None and str(session_value_hindi, 'utf-8') == "True":
            #     text = "/language_change"
            # else:
            # nlg_call["message"] = "/change_language_from_kannada_to_hindi"
        red_telugu.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"telugu","False",ex=300)
        bot_responses = await generate_response(nlg_call)
        return bot_responses
    
    # if "మరాఠీ" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
    #     if intent == "language_change":
    #         # if session_value_hindi is not None and str(session_value_hindi, 'utf-8') == "True":
    #         #     text = "/language_change"
    #         # else:
    #         # nlg_call["message"] = "/change_language_from_kannada_to_hindi"
    #         red_telugu.set(str(sender_id)+"marathi", "True", ex=300)
    #         red_marathi.set(str(sender_id)+"telugu","False",ex=300)
    #         bot_responses = await generate_response_marathi(nlg_call)
    #         return bot_responses
    
    # if "బెంగాలీ" in text or "బంగ్లా" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
    #     if intent == "language_change":
    #         # if session_value_hindi is not None and str(session_value_hindi, 'utf-8') == "True":
    #         #     text = "/language_change"
    #         # else:
    #         # nlg_call["message"] = "/change_language_from_kannada_to_hindi"
    #         red_telugu.set(str(sender_id)+"bengali", "True", ex=300)
    #         red_bengali.set(str(sender_id)+"telugu","False",ex=300)
    #         bot_responses = await generate_response_bengali(nlg_call)
    #         return bot_responses
    
    if "మలయాళం" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
        # if intent == "language_change":
            # if session_value_hindi is not None and str(session_value_hindi, 'utf-8') == "True":
            #     text = "/language_change"
            # else:
            # nlg_call["message"] = "/change_language_from_kannada_to_hindi"
        red_telugu.set(str(sender_id)+"malayalam", "True", ex=300)
        red_malayalam.set(str(sender_id)+"telugu","False",ex=300)
        bot_responses = await generate_response_malayalam(nlg_call)
        return bot_responses

    # if "పంజాబీ" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
    #     if intent == "language_change":
    #         red_telugu.set(str(sender_id)+"punjabi", "True", ex=300)
    #         red_punjabi.set(str(sender_id)+"telugu","False",ex=300)
    #         bot_responses = await generate_response_punjabi(nlg_call)
    #         return bot_responses
    # if "గుజరాతీ" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     # session_value_hindi = red_hindi.get(str(sender_id)+"kannada")
    #     if intent == "language_change":
    #         red_telugu.set(str(sender_id)+"gujarati", "True", ex=300)
    #         red_gujarati.set(str(sender_id)+"telugu","False",ex=300)
    #         bot_responses = await generate_response_gujarati(nlg_call)
    #         return bot_responses

    # url = "http://localhost:8818/webhooks/rest/webhook"
    url = "http://20.127.208.146/core_telugu/webhooks/rest/webhook"
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)

    if bot_response.get("custom", None) is None:
        bot_response["custom"] = {}
    bot_response["custom"]["tts"] = "te-IN"
    bot_response["custom"]["stt"] = "te-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "te-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template_name>")[0]
        template_name=item["text"].split("<template_name>")[1]
        item['text']=item["text"].split("<template_name>")[0]
        hash_object = hashlib.md5(message.encode('utf-8'))
        file_name = str(hash_object.hexdigest())
        item['force']=1
        item[
            "voice_data"] = "http://adhar.saarthi.ai/aadhar_tts/wav?message={message}&template_name={template_name}&language=" \
                             "{language}".format(message=message, template_name=template_name, language="telugu")
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses

    return bot_response

async def generate_response_malayalam(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    print("Malayalam NLG call:",nlg_call)
    sender_id = nlg_call.get("sender", None)
    request_id = nlg_call.get("request_id", None)
    user_id = nlg_call.get("user_id", None)
    text = nlg_call.get("message", None)

    if text:
        text = text.lower()
    if text == "/pre_emi" or text == "/post_emi_dpd7" or text == "post_emi_dpd15" or text == "post_emi_dpd15+" or text == "ptp_breached" or text == "/ptp_breached" or text == "/call_after_bounce" or text == "/motilal_oswal_outbound" or text == "/wishfin_poc":
        text = "/initial_message"
    if sender_id is None or request_id is None or user_id is None or text is None:
        bot_response = {"error": "Arguments missing"}
        return bot_response

    data = red.hget("cz","5")
    if data == "no":
        if text != "/initial_message":
            nlu = nlg_call.get("nlu_data", None)
            ner = nlg_call.get("ner_data",None)
            if ner is not None and ner !="":
                text = text +" "+"<nlu>"+str(nlu)+"<ner>"+str(ner)
            else:
                text = text +" "+"<nlu>"+str(nlu)

    session_value_kannada_old = red_malayalam.get(str(sender_id)+"kannada")
    session_value_hindi_old = red_malayalam.get(str(sender_id)+"hindi")
    session_value_tamil_old=red_malayalam.get(str(sender_id)+"tamil")
    session_value_telugu_old=red_malayalam.get(str(sender_id)+"telugu")
    # session_value_bengali_old=red_malayalam.get(str(sender_id)+"bengali")
    # session_value_punjabi_old = red_malayalam.get(str(sender_id)+"punjabi")
    # session_value_marathi_old = red_malayalam.get(str(sender_id)+"marathi")
    session_value_english_old = red_malayalam.get(str(sender_id)+"english")
    # session_value_gujarati_old = red_malayalam.get(str(sender_id)+"gujarati")

    print("Malayalam old:",session_value_hindi_old)
    if session_value_hindi_old is not None and str(session_value_hindi_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_hindi(nlg_call)
        red_malayalam.set(str(sender_id)+"hindi", "True", ex=300)
        return bot_responses
    if session_value_kannada_old is not None and str(session_value_kannada_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_kannada(nlg_call)
        red_malayalam.set(str(sender_id)+"kannada", "True", ex=300)
        return bot_responses
    if session_value_tamil_old is not None and str(session_value_tamil_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_tamil(nlg_call)
        red_malayalam.set(str(sender_id)+"tamil", "True", ex=300)
        return bot_responses
    if session_value_telugu_old is not None and str(session_value_telugu_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response_telugu(nlg_call)
        red_malayalam.set(str(sender_id)+"telugu", "True", ex=300)
        return bot_responses
    # if session_value_bengali_old is not None and str(session_value_bengali_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_bengali(nlg_call)
    #     red_malayalam.set(str(sender_id)+"bengali", "True", ex=300)
    #     return bot_responses
    # if session_value_punjabi_old is not None and str(session_value_punjabi_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_punjabi(nlg_call)
    #     red_malayalam.set(str(sender_id)+"punjabi", "True", ex=300)
    #     return bot_responses
    # if session_value_marathi_old is not None and str(session_value_marathi_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_marathi(nlg_call)
    #     red_malayalam.set(str(sender_id)+"marathi", "True", ex=300)
    #     return bot_responses
    if session_value_english_old is not None and str(session_value_english_old, 'utf-8') == "True":
        print("*********************")
        bot_responses = await generate_response(nlg_call)
        red_malayalam.set(str(sender_id)+"english", "True", ex=300)
        return bot_responses
    # if session_value_gujarati_old is not None and str(session_value_gujarati_old, 'utf-8') == "True":
    #     print("*********************")
    #     bot_responses = await generate_response_gujarati(nlg_call)
    #     red_malayalam.set(str(sender_id)+"gujarati", "True", ex=300)
    #     return bot_responses

    if "ഹിന്ദി" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # if intent == "language_change":
        red_malayalam.set(str(sender_id)+"hindi", "True", ex=300)
        red_hindi.set(str(sender_id)+"malayalam","False",ex=300)
        bot_responses = await generate_response_hindi(nlg_call)
        return bot_responses
    if "കന്നഡ" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # if intent == "language_change":
        red_malayalam.set(str(sender_id)+"kannada", "True", ex=300)
        red_kannada.set(str(sender_id)+"malayalam","False",ex=300)
        bot_responses = await generate_response_kannada(nlg_call)
        return bot_responses
    if "തമിഴ്" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # if intent == "language_change":
        red_malayalam.set(str(sender_id)+"tamil", "True", ex=300)
        red_tamil.set(str(sender_id)+"malayalam","False",ex=300)
        bot_responses = await generate_response_tamil(nlg_call)
        return bot_responses
    if "തെലുങ്ക്" in text or "തെലുങ്കു" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # if intent == "language_change":
        red_malayalam.set(str(sender_id)+"telugu", "True", ex=300)
        red_telugu.set(str(sender_id)+"malayalam","False",ex=300)
        bot_responses = await generate_response_telugu(nlg_call)
        return bot_responses
    # if "ബംഗ്ലാ" in text or "ബംഗാളി" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_malayalam.set(str(sender_id)+"bengali", "True", ex=300)
    #         red_bengali.set(str(sender_id)+"malayalam","False",ex=300)
    #         bot_responses = await generate_response_bengali(nlg_call)
    #         return bot_responses
            
    # if "പഞ്ചാബി" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_malayalam.set(str(sender_id)+"punjabi", "True", ex=300)
    #         red_punjabi.set(str(sender_id)+"malayalam","False",ex=300)
    #         bot_responses = await generate_response_punjabi(nlg_call)
    #         return bot_responses

    # if "മറാത്തി" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_malayalam.set(str(sender_id)+"marathi", "True", ex=300)
    #         red_marathi.set(str(sender_id)+"malayalam","False",ex=300)
    #         bot_responses = await generate_response_marathi(nlg_call)
    #         return bot_responses
    
    if "ഇംഗ്ലീഷ്" in text:
        # intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
        # print(intent)
        # intent = intent["label"][0]["name"]
        # if intent == "language_change":
        red_malayalam.set(str(sender_id)+"english", "True", ex=300)
        red_english.set(str(sender_id)+"malayalam","False",ex=300)
        bot_responses = await generate_response(nlg_call)
        return bot_responses
    # if "ഗുജറാത്തി" in text:
    #     intent = requests.post('http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score', json={"data": str(text)}).json()
    #     print(intent)
    #     intent = intent["label"][0]["name"]
    #     if intent == "language_change":
    #         red_malayalam.set(str(sender_id)+"gujarati", "True", ex=300)
    #         red_gujarati.set(str(sender_id)+"malayalam","False",ex=300)
    #         bot_responses = await generate_response_malayalam(nlg_call)
    #         return bot_responses

    # url = "http://localhost:8939/webhooks/rest/webhook"
    # url = "http://20.127.208.146/core_malayalam/webhooks/rest/webhook"
    url = "http://localhost:8850/webhooks/rest/webhook"
    bot_response = await call_bot(url, sender_id, request_id, user_id, text)

    if bot_response.get("custom", None) is None:
        bot_response["custom"] = {}
    bot_response["custom"]["tts"] = "ml-IN"
    bot_response["custom"]["stt"] = "ml-IN"
    bot_response["custom"]["tts_gender"] = "FEMALE"
    bot_response["custom"]["tts_speaking_rate"] = "0.9"
    bot_response["custom"]["tts_voice_name"] = "ml-IN-Standard-A"
    if "time_limit" not in bot_response.get("custom"):
        bot_response["custom"]["time_limit"] = 8

    bot_response["sender_id"] = sender_id
    bot_response["request_id"] = request_id
    bot_response["user_id"] = user_id

    bot_utterances = bot_response.get("data")
    final_bot_responses = []
    for item in bot_utterances:
        message = item["text"].split("<template_name>")[0]
        template_name=item["text"].split("<template_name>")[1]
        item['text']=item["text"].split("<template_name>")[0]
        hash_object = hashlib.md5(message.encode('utf-8'))
        file_name = str(hash_object.hexdigest())
        item['force'] = 1
        item["voice_data"] = "{audio_url}/wav?message={message}&template_name={template_name}&language=" \
                            "{language}".format(message=message, template_name=template_name, language="malayalam",audio_url=audio_url)
        final_bot_responses.append(item)
    bot_response["data"] = final_bot_responses

    return bot_response
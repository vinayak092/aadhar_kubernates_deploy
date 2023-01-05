import requests
import csv
import datetime

def get_sender_id(data):
    return data['sender_id'] if 'sender_id' in data else None


def get_user_id(data):
    return data['user_id'] if 'user_id' in data else None

def get_sender_id(data):
    return data["sender_id"] if "sender_id" in data else None
    
def get_request_id(data):
    return data['request_id'] if 'request_id' in data else None


def get_event_type(data):
    return data['event'] if 'event' in data else None


def get_intent_name(data):
    if 'parse_data' in data:
        if 'intent' in data['parse_data']:
            return data['parse_data']['intent']['name']
        else:
            return None
    else:
        return None


def get_intent_confidence(data):
    if 'parse_data' in data:
        if 'intent' in data['parse_data']:
            return data['parse_data']['intent']['confidence']
        else:
            return None
    else:
        return None


def get_entity(data):
    if 'parse_data' in data:
        if 'entities' in data['parse_data']:
            entities = data['parse_data']['entities']

            if entities:
                return entities
        else:
            return None
    else:
        return None


def get_action_name(data):
    if data['event'] == 'action' and data['name'] != 'action_listen':
        return data['name']
    return None


def get_action_confidence(data):
    if data['event'] == 'action' and data['name'] != 'action_listen':
        return data['confidence']
    return None


def get_timestamp(data):
    return data['timestamp']
def get_disposition_id(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "disposition_id" in data["data"]["custom"]:
                if data["data"]["custom"]["disposition_id"] is not None:
                    return data["data"]["custom"]["disposition_id"]
                return ""
            return ""
        return ""
    return ""
def get_delay_reason(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "delay_reason" in data["data"]["custom"]:
                if data["data"]["custom"]["delay_reason"] is not None:
                    return data["data"]["custom"]["delay_reason"]
                return ""
            return ""
        return ""
    return ""
def get_emi_amount(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "outstanding_payment" in data["data"]["custom"]:
                if data["data"]["custom"]["outstanding_payment"] is not None:
                    return data["data"]["custom"]["outstanding_payment"]
                return ""
            return ""
        return ""
    return ""
def get_language(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "language" in data["data"]["custom"]:
                if data["data"]["custom"]["language"] is not None:
                    return data["data"]["custom"]["language"]
                return ""
            return ""
        return ""
    return ""
def get_emi_flow(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "flow_type" in data["data"]["custom"]:
                if data["data"]["custom"]["flow_type"] is not None:
                    return data["data"]["custom"]["flow_type"]
                return ""
            return ""
        return ""
    return ""
def get_ptp_date(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "ptp_date" in data["data"]["custom"]:
                if data["data"]["custom"]["ptp_date"] is not None:
                    return data["data"]["custom"]["ptp_date"]
                return ""
            return ""
        return ""
    return ""
def get_response_time(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "response_time" in data["data"]["custom"]:
                if data["data"]["custom"]["response_time"] is not None:
                    return data["data"]["custom"]["response_time"]
                return ""
            return ""
        return ""
    return ""
def get_partial_amount(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "partial_amount" in data["data"]["custom"]:
                if data["data"]["custom"]["partial_amount"] is not None:
                    return data["data"]["custom"]["partial_amount"]
                return ""
            return ""
        return ""
    return ""
def get_customer_name(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "customer_name" in data["data"]["custom"]:
                if data["data"]["custom"]["customer_name"] is not None:
                    return data["data"]["custom"]["customer_name"]
                return ""
            return ""
        return ""
    return ""
def get_loan_id(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "loan_id" in data["data"]["custom"]:
                if data["data"]["custom"]["loan_id"] is not None:
                    return data["data"]["custom"]["loan_id"]
                return ""
            return ""
        return ""
    return ""
def get_emi_amount(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "emi_amount" in data["data"]["custom"]:
                if data["data"]["custom"]["emi_amount"] is not None:
                    return data["data"]["custom"]["emi_amount"]
                return ""
            return ""
        return ""
    return ""
def get_due_date(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "due_date" in data["data"]["custom"]:
                if data["data"]["custom"]["due_date"] is not None:
                    return data["data"]["custom"]["due_date"]
                return ""
            return ""
        return ""
    return ""
def get_payment_link(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "payment_link" in data["data"]["custom"]:
                if data["data"]["custom"]["payment_link"] is not None:
                    return data["data"]["custom"]["payment_link"]
                return ""
            return ""
        return ""
    return ""
def get_ptp_recheck(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "ptp_recheck" in data["data"]["custom"]:
                if data["data"]["custom"]["ptp_recheck"] is not None:
                    return data["data"]["custom"]["ptp_recheck"]
                return ""
            return ""
        return ""
    return ""
def get_sheet_name(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "sheet_name" in data["data"]["custom"]:
                if data["data"]["custom"]["sheet_name"] is not None:
                    return data["data"]["custom"]["sheet_name"]
                return ""
            return ""
        return ""
    return ""
def get_payment_status(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "payment_status" in data["data"]["custom"]:
                if data["data"]["custom"]["payment_status"] is not None:
                    return data["data"]["custom"]["payment_status"]
                return ""
            return ""
        return ""
    return ""

def payment_link(response):
    # TODO need to update the bot responses according to status of the message sent ->
    #  means if message not sent update the bot responses
    phone_number = get_user_id(response)
    # if not phone_number.startswith("91"):
    #     phone_number = "91" + phone_number
    # customer_name=get_customer_name(response)
    loan_id=get_loan_id(response)
    total_emi_amount=get_emi_amount(response)
    due_date=get_due_date(response)
    payment_link=get_payment_link(response)
    if payment_link!="":
        message="""Dear customer, Greetings from Avail Finance! Your CreditATM Loan ID: {loan_id} is due for: {emi_amount} on: {due_date}. Pay your dues today to reactivate your credit limit. You can pay by clicking on the link {payment_link} or through the Avail app.""".\
            format(loan_id=loan_id,total_emi_amount=total_emi_amount, due_date=due_date,payment_link=payment_link)
        print("Sending message to phone number", phone_number)
        # headers = {
        #     "api-key": "Ad9ba96c1c7d12ee451e01fe20dcc0fc3",
        # }

        try:
            data = {
                "login":"Avail_iKontel_Saarthi",
                "passwd":"avail@321",
                "version":"v1.0",
                "msisdn":phone_number,
                "msg_type":"text",
                "msg":message,
                "sender_id":"iavail"
            }
            print(data)
            # start_time = datetime.datetime.now()
            response_qs = requests.get(
                "https://msg2all.com/TRANSAPI/sendsms.jsp",
                params=data,
            ).json()
            # end_time = datetime.datetime.now()
            # print("Time taken to send the message", end_time - start_time)
            print(response_qs)
            if response_qs.get("recipients"):
                print(response_qs)
        except Exception as e:
            print(e)
        
def store_in_csv(user_id,disposition_id,ptp_date,partial_amount,delay_reason,response_time,ptp_recheck,sheet_name,session_id,loan_id):
    try:
        with open('call_logs.csv', 'r+', newline='') as file:
            data = csv.reader(file)
            writer = csv.writer(file)
            current_date = datetime.datetime.now()
            if len(list(data)) == 0:
                writer.writerows(
                    [["date", "phone number", "disposition id", "ptp_date", "partial_amount","delay_reason","time","ptp_recheck","sheet_name","session_id","loan_id"], [
                        current_date.strftime("%d/%m/%Y"), user_id, disposition_id, ptp_date,partial_amount,delay_reason,response_time,ptp_recheck,sheet_name,session_id,loan_id]])
            else:
                writer.writerow([current_date.strftime("%d/%m/%Y"), user_id, disposition_id,ptp_date, partial_amount,delay_reason,response_time,ptp_recheck,sheet_name,session_id,loan_id])
    except IOError:
        with open('call_logs.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            current_date = datetime.datetime.now()
            writer.writerows(
                [["date", "phone number", "disposition id", "ptp_date", "partial_amount","delay_reason","time","ptp_recheck","sheet_name","session_id","loan_id"], [
                    current_date.strftime("%d/%m/%Y"), user_id, disposition_id, ptp_date,partial_amount,delay_reason,response_time,ptp_recheck,sheet_name,session_id,loan_id]])
# def write_to_database(response):
#
#     sender_id = get_sender_id(response)
#     user_id = get_user_id(response)
#     request_id = get_request_id(response)
#     event_type = get_event_type(response)
#     event = response.copy()
#     intent = get_intent_name(response)
#     intent_confidence = get_intent_confidence(response)
#     entity = get_entity(response)
#     action_name = get_action_name(response)
#     action_confidence = get_action_confidence(response)
#     timestamp = get_timestamp(response)
#
#     try:
#         database.connect(reuse_if_open=True)
#         NaviEnglishEvents.insert(sender_id=sender_id, user_id=user_id, request_id=request_id,
#                     event_type=event_type, event=event, intent=intent, intent_confidence=intent_confidence,
#                     entity=entity, action_name=action_name, action_confidence=action_confidence,
#                     timestamp=timestamp).execute()
#         database.close()
#     except Exception as e:
#         print(str(e))

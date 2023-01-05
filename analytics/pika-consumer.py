# from actions.utils.helper import store_call_log
import json
import pika
import argparse, sys, os
from rasa.utils.endpoints import read_endpoint_config
import requests
import csv
import datetime
from analytics_helper import *
from settings import *
# from kredit_english_db import *

connection = None
f = open("api_logs.txt", "w+")


def create_arg_parser():
    # Creates and returns the ArgumentParser object
    parser = argparse.ArgumentParser(description='Argument parser for reading enpoint file.')
    parser.add_argument('--endpoints', help='Path to endpoint file.')
    return parser


def _callback(channel, method, properties, body):
    # Do something useful with your incoming message body here, e.g.
    # saving it to a database

    response = json.loads(body)
    print('Received event {}'.format(response))

    if response['event'] != 'action' or (response['event'] == 'action' and response['name'] != 'action_listen'):
        # write_to_database(response)
        # store_call_logs(response)
        print("written..")
    if response['event'] != 'action' or (response['event'] == 'action' and response['name'] != 'action_listen'):
        store_call_logs(response)


def write_to_database(response):
    sender_id = get_sender_id(response)
    user_id = get_user_id(response)
    request_id = get_request_id(response)
    event_type = get_event_type(response)
    event = response.copy()
    intent = get_intent_name(response)
    intent_confidence = get_intent_confidence(response)
    entity = get_entity(response)
    action_name = get_action_name(response)
    action_confidence = get_action_confidence(response)
    timestamp = get_timestamp(response)

    try:
        database.connect(reuse_if_open=True)
        KreditBeeEnglishEvents.insert(sender_id=sender_id, user_id=user_id, request_id=request_id,
                                 event_type=event_type, event=event, intent=intent,
                                 intent_confidence=intent_confidence,
                                 entity=entity, action_name=action_name, action_confidence=action_confidence,
                                 timestamp=timestamp).execute()
        database.close()
    except Exception as e:
        print(str(e))


def send_message(response):
    print("********** Sending ************")
    print("Response:", response)
    payment_link(response)


def store_call_logs(response):
    print("********Response:", response)
    user_id = get_user_id(response)
    campaign_name = "KreditBee"
    disposition_id = get_disposition_id(response)
    delay_reason = get_delay_reason(response)
    ptp_date = get_ptp_date(response)
    response_time = get_response_time(response)
    partial_amount = get_partial_amount(response)
    ptp_recheck = get_ptp_recheck(response)
    sheet_name=get_sheet_name(response)
    payment_status = get_payment_status(response)
    session_id = response['sender_id']
    loan_id = get_loan_id(response)
    print("Disposition Id:", disposition_id)
    if disposition_id != "":
        ###### Storing in CSV #############

        store_in_csv(user_id, disposition_id, ptp_date, partial_amount, delay_reason, response_time, ptp_recheck,sheet_name,session_id,loan_id)

        ####### Sending to Dashboard ##############

        data = {
            "phone_number": user_id,
            "campaignName": campaign_name,
            "dispositionName": disposition_id,
            "ptp_date": ptp_date,
            "reason": delay_reason,
            "response_time": response_time,
            "partial_amount": partial_amount,
            "ptp_recheck": ptp_recheck,
            "sheet_name":sheet_name,
            "sessionId":response['sender_id'],
            "loan_id":loan_id
        }
        print("Data:", data)
        print("++++++++ Sending ++++++++++++")
        r = requests.post("https://dashboard.saarthi.ai/apiameyo/bot/", json=data,
                          headers={'Content-type': 'application/json'})
        f.write(str(r.status_code))
        print(r.status_code)


def main(endpoint_file):
    # Initiate parser

    config_obj = read_endpoint_config(endpoint_file, endpoint_type="event_broker")
    print(config_obj)

    username = config_obj.kwargs['username'] if 'username' in config_obj.kwargs else None
    password = config_obj.kwargs['password'] if 'password' in config_obj.kwargs else None
    queue = config_obj.kwargs['queue'] if 'queue' in config_obj.kwargs else None

    print()
    print("CREDENTIALS: username: %s, password: %s, queue-name: %s" % (username, password, queue))
    if username and password and queue:
        # RabbitMQ credentials with username and password
        credentials = pika.PlainCredentials(username, password)

        # Pika connection to the RabbitMQ host - typically 'rabbit' in a
        # docker environment, or 'localhost' in a local environment
        global connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', credentials=credentials, heartbeat=600,
                                      blocked_connection_timeout=300))

        # start consumption of channel
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_consume(queue=queue,
                              on_message_callback=_callback,
                              auto_ack=True)

        print("======================================================")
        print(' [*] Waiting for messages. To exit press CTRL+C')
        print("=======================================================")
        print()

        channel.start_consuming()

    else:
        print("Incorrect eventbroker data in endpoints file...")


if __name__ == '__main__':

    try:
        argparser = create_arg_parser()
        parsed_arguments = argparser.parse_args(sys.argv[1:])
        endpoint_file = parsed_arguments.endpoints
        main(endpoint_file)
    except KeyboardInterrupt:
        print('Interrupted')
        print('Closing connection..')
        connection.close()
        # database.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

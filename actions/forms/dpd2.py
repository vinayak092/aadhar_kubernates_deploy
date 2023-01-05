from datetime import datetime
from email import utils
import time
from actions.utils.common_imports import *
from actions.utils.helper import *
import handle_bulk_data
helper = Helper()
class  Aadhar_Predue_form(FormAction):
    def name(self):
        return ""
    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        availability_status = tracker.get_slot("availability_status")
        not_available = tracker.get_slot("not_available")
        call_back = tracker.get_slot("call_back")
        available_two = tracker.get_slot("available_two")
        payment_confirmation = tracker.get_slot("payment_confirmation")
        delay_reason = tracker.get_slot("delay_reason")
        if stop_conversation == "TRUE":
            return []
        if payment_confirmation == "delay_reason":
            return ["delay_reason"]
        if payment_confirmation == "call_back":
            return ["call_back"]
        if not_available == "call_back":
            return ["call_back"]
        if availability_status == "not_available":
            return ["not_available"]
        if availability_status == "payment_confirmation":
            return ["payment_confirmation"]
        if availability_status == "call_back":
            return ["call_back"]
        return ["availability_status"]

        if stop_conversation == "TRUE":
            return []      
        # if third_party == "available_two":
        #     return ["available_two"]
        # if third_party == "availability_status":
        #     return ["availability_status"]
        if payment_confirmation == "delay_reason":
            return ["delay_reason"]
        if payment_confirmation == "call_back":
            return ["call_back"]     
        if payment_confirmation == "third_party":
            return ["third_party"]
        if third_party == "available_two":
            return ["available_two"]
        if third_party == "availability_status":
            return ["availability_status"] 
        if third_party == "payment_confirmation":
            return ["payment_confirmation"]
        if third_party == "call_back":
            return ["call_back"]     
        if delay_reason == "call_back":
            return ["call_back"]
        
        # if third_party == "available_two":
        #     return ["available_two"]
        # if third_party == "availability_status":
        #     return ["availability_status"] 
        # if third_party == "payment_confirmation":
        #     return ["payment_confirmation"]
        # if third_party == "call_back":
        #     return ["call_back"]
        if not_available == "call_back":
            return ["call_back"]
        if not_available == "third_party":
            return ["third_party"]
        if availability_status == "not_available":
            return ["not_available"]
        if availability_status == "third_party":
            return ["third_party"]
        if availability_status == "payment_confirmation":
            return ["payment_confirmation"]
        if availability_status == "call_back":
            return ["call_back"]

        return ["availability_status"]
    def get_delay_reason(self,value=None):
        return [
            self.from_intent(intent="business_loss", value=value),
            self.from_intent(intent="insufficient_funds", value=value),
            self.from_intent(intent="job_loss", value=value),
            self.from_intent(intent="family_dispute", value=value),
            self.from_intent(intent="branch_issue", value=value),
            self.from_intent(intent="account_not_working", value=value),
            self.from_intent(intent="personal_issue",value=value),
            self.from_intent(intent="salary_issue",value=value),
        ]
    def slot_mappings(self):
        return{
            "availability_status": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "deny",value = "FALSE"),
                self.from_intent(intent = "third_party_contact",value ="FALSE"),
                self.from_intent(intent = "disagree_to_proceed",value ="FALSE"),
                self.from_intent(intent = "inform_wrong_info", value="wrong_number"),
                self.from_intent(intent = "wrong_number", value="wrong_number"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),
            ],
            "not_available": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "disagree_to_proceed",value ="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "deny",value = "FALSE"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),
                self.from_intent(intent = "inform_wrong_info", value="wrong_number"),
                self.from_intent(intent = "wrong_number", value="wrong_number"),
            ],
            "call_back": [
                self.from_intent(intent = "disagree_to_proceed",value ="inform_call_later"),
                self.from_intent(intent = "deny",value = "inform_call_later"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),
                self.from_intent(intent = "disagree_to_pay", value="inform_call_later"),
                self.from_intent(intent = "wrong_number", value="wrong_number"),
                self.from_intent(intent = "inform_wrong_info", value="wrong_number"),
            ],
             "payment_confirmation": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value ="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "disagree_to_proceed",value ="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "deny",value = "FALSE"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),
                self.from_intent(intent = "out_of_context",value = "out_of_context"),
                self.from_intent(intent = "inform_wrong_info",value = "inform_wrong_info"),
                self.from_intent(intent = "ask_bounce_charge_details",value = "know_more"),      
            ],
             "delay_reason": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value ="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "deny",value = "FALSE"),
                self.from_intent(intent = "disagree_to_proceed",value ="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),   
            ],
        }
    @staticmethod
    def _should_request_slot(tracker,slot_name):
        return tracker.get_slot(slot_name) is None
    def request_next_slot(
        self,
        dispatcher:"CollectingDispatcher",
        tracker:"Tracker",
        domain:Dict[Text,Any]
        ):
        total_emi_amount = tracker.get_slot("total_emi_amount")
        due_date = tracker.get_slot("due_date")
        sheet_name = tracker.get_slot("sheet_name")
        emi_flow = tracker.get_slot("emi_flow")
        loan_id = tracker.get_slot("loan_id")
        customer_name = tracker.get_slot("customer_name")
        link_status= tracker.get_slot("link_status")
        for slot in self.required_slots(tracker):
            trail_count = tracker.get_slot("trail_count")
            if self._should_request_slot(tracker,slot):
                print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
                if slot == "availability_status":
                    if trail_count is None:
                        trail_count = 0
                        dispatcher.utter_template("utter_greet_2_pre_due_aadhar",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="initial_message",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_greet_2_pre_due_aadhar",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="initial_message",emi_flow=emi_flow)
                if slot == "not_available":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_busy_not_available_pre_due_aadhar",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="UB",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_busy_not_available_pre_due_aadhar",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="UB",emi_flow=emi_flow)
                if slot == "call_back":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_busy_not_available_2_pre_due_aadhar",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="UB",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_busy_not_available_2_trim_pre_due_aadhar",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="UB",emi_flow=emi_flow)
                if slot == "payment_confirmation":
                    if trail_count is None:
                        trail_count = 0
                        if link_status == "YES":
                            dispatcher.utter_template("utter_greet_yes_pre_due_aadhar", tracker,emi_amount=total_emi_amount,due_date=due_date)
                        else:
                            dispatcher.utter_template("utter_greet_yes_2_pre_due_aadhar", tracker,emi_amount=total_emi_amount,due_date=due_date) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="PIC",emi_flow=emi_flow)
                    else:
                        if link_status == "YES":
                            dispatcher.utter_template("utter_greet_yes_pre_due_aadhar", tracker,emi_amount=total_emi_amount,due_date=due_date)
                        else:
                            dispatcher.utter_template("utter_greet_yes_2_pre_due_aadhar", tracker,emi_amount=total_emi_amount,due_date=due_date) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="PIC",emi_flow=emi_flow)
                if slot == "delay_reason":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_refuse_to_pay_time_pre_due_aadhar", tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="RTP",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_refuse_to_pay_time_pre_due_aadhar",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="RTP",emi_flow=emi_flow)
                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1)]
    @staticmethod
    def validate_availability_status(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any],
    ):
        print("The value comes to this function is, ",value)
        total_emi_amount = tracker.get_slot("total_emi_amount")
        due_date = tracker.get_slot("due_date")
        sheet_name = tracker.get_slot("sheet_name")
        emi_flow = tracker.get_slot("emi_flow")
        loan_id = tracker.get_slot("loan_id")
        customer_name = tracker.get_slot("customer_name")
        link_status = tracker.get_slot("link_status")
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
            disposition_id="PIC",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"availability_status":"payment_confirmation","trail_count":None}
        elif value ==  "FALSE":    
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="UB",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"availability_status":"not_available","trail_count":None}
        elif value == "inform_call_later":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            if entities:
                if length>1:
                    time = entities[1]["value"]
                    date = entities[0]["value"]
                    callback_time = date+" "+time
                    print("The value of time",time)
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"availability_status":value,"stop_conversation": "TRUE"}
                elif length==1:
                    date = entities[0]["value"]
                    callback_time = date
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"availability_status":value,"stop_conversation": "TRUE"}
            else:
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"availability_status":"call_back","trail_count":None}
        elif value ==  "wrong_number": 
            dispatcher.utter_template("utter_wrong_number_pre_due_aadhar", tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="NRPC",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"availability_status": value,"stop_conversation": "TRUE"}
        return{"availability_status":None}
    @staticmethod
    def validate_not_available(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any], 
    ):
        total_emi_amount = tracker.get_slot("total_emi_amount")
        due_date = tracker.get_slot("due_date")
        sheet_name = tracker.get_slot("sheet_name")
        emi_flow = tracker.get_slot("emi_flow")
        loan_id = tracker.get_slot("loan_id")
        customer_name = tracker.get_slot("customer_name")
        user_message = tracker.latest_message.get("text")
        if value == "TRUE":
            dispatcher.utter_template("utter_agreed_to_proceed_pre_due_aadhar", tracker,emi_amount=total_emi_amount,due_date=due_date)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"not_available": value,"trail_count":None, "stop_conversation": "TRUE"}   
        elif value == "FALSE":  
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="UB",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"not_available": "call_back","trail_count":None}
        elif value == "inform_call_later":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            if entities:
                if length>1:
                    time = entities[1]["value"]
                    date = entities[0]["value"]
                    callback_time = date+" "+time
                    print("The value of time",time)
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"not_available":value,"stop_conversation": "TRUE"}
                elif length==1:
                    date = entities[0]["value"]
                    callback_time = date
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"not_available":value,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_call_back_time_not_given_pre_due_aadhar",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"not_available":value,"stop_conversation": "TRUE"}
        elif value == "wrong_number":
            dispatcher.utter_template("utter_wrong_number_pre_due_aadhar", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="NRPC",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"not_available": value,"stop_conversation": "TRUE"}
        return{"not_available":None}
    @staticmethod
    def validate_call_back(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any]
    ):
        total_emi_amount = tracker.get_slot("total_emi_amount")
        due_date = tracker.get_slot("due_date")
        sheet_name = tracker.get_slot("sheet_name")
        emi_flow = tracker.get_slot("emi_flow")
        loan_id = tracker.get_slot("loan_id")
        customer_name = tracker.get_slot("customer_name")
        user_message = tracker.latest_message.get("text")
        if value ==  "inform_call_later":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            if entities:
                if length>1:
                    time = entities[1]["value"]
                    date = entities[0]["value"]
                    callback_time = date+" "+time
                    print("The value of time",time)
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"call_back":value,"stop_conversation": "TRUE"}
                elif length==1:
                    date = entities[0]["value"]
                    callback_time = date
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"call_back":value,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_call_back_time_not_given_pre_due_aadhar",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"call_back":value,"stop_conversation": "TRUE"}
        elif value == "wrong_number":
            dispatcher.utter_template("utter_wrong_number_pre_due_aadhar",tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
            return {"call_back":value,"stop_conversation": "TRUE"}
        return{"call_back":None}
    @staticmethod
    def validate_payment_confirmation(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any]
    ):
        total_emi_amount = tracker.get_slot("total_emi_amount")
        due_date = tracker.get_slot("due_date")
        sheet_name = tracker.get_slot("sheet_name")
        emi_flow = tracker.get_slot("emi_flow")
        loan_id = tracker.get_slot("loan_id")
        customer_name = tracker.get_slot("customer_name")
        user_message = tracker.latest_message.get("text")
        link_status = tracker.get_slot("link_status")
        if value ==  "TRUE":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            print("The value of entity length",len(entities))
            if entities:
                for entity in entities:
                    given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                    given_date = given_date.strftime("%d-%m-%Y")
                    today = datetime.datetime.now()
                    today = today.strftime("%d-%m-%Y")
                    d1 = datetime.datetime.strptime(today, "%d-%m-%Y")
                    d2 = datetime.datetime.strptime(given_date, "%d-%m-%Y")
                    val = d2-d1
                    days = val.days
                    if days<=0:
                        if link_status == "YES":
                            dispatcher.utter_template("utter_agree_to_pay_pre_due_aadhar",tracker)
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                            return {"payment_confirmation":value,"stop_conversation": "TRUE"}
                        else:
                            dispatcher.utter_template("utter_agree_pay_2_pre_due_aadhar",tracker)
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                            return {"payment_confirmation":value,"stop_conversation": "TRUE"}
                    else:
                        dispatcher.utter_template("utter_refuse_to_pay_time_pre_due_aadhar",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="",flag=DEFAULT_FLAG,emi_flow=emi_flow)
                        return {"payment_confirmation":"delay_reason","trail_count":None}       
            else:
                if link_status == "YES":
                    dispatcher.utter_template("utter_agree_to_pay_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                    return {"payment_confirmation":value,"stop_conversation": "TRUE"}
                else:
                    dispatcher.utter_template("utter_agree_pay_2_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                    return {"payment_confirmation":value,"stop_conversation": "TRUE"}
        elif value ==  "FALSE":
            dispatcher.utter_template("utter_refuse_to_pay_time_pre_due_aadhar",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}
        elif value == "inform_call_later":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            if entities:
                if length>1:
                    time = entities[1]["value"]
                    date = entities[0]["value"]
                    callback_time = date+" "+time
                    print("The value of time",time)
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"availability_status":value,"stop_conversation": "TRUE"}
                elif length==1:
                    date = entities[0]["value"]
                    callback_time = date
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"availability_status":value,"stop_conversation": "TRUE"}
            else:
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"availability_status":"call_back","trail_count":None}
        elif value == "out_of_context":
            dispatcher.utter_template("utter_out_of_scope_pre_due_aadhar",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="outofcontext",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}
        elif value == "inform_wrong_info":
            dispatcher.utter_template("utter_customer_dispute_in_loan_pre_due_aadhar",tracker,cycle_date=due_date)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}
        elif value == "know_more":
            dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}
        return{"payment_confirmation":None}
    @staticmethod
    def validate_delay_reason(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any], 
    ):
        total_emi_amount = tracker.get_slot("total_emi_amount")
        due_date = tracker.get_slot("due_date")
        sheet_name = tracker.get_slot("sheet_name")
        emi_flow = tracker.get_slot("emi_flow")
        loan_id = tracker.get_slot("loan_id")
        customer_name = tracker.get_slot("customer_name")
        link_status = tracker.get_slot("link_status")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            if link_status == "YES":
                dispatcher.utter_template("utter_agree_to_pay_pre_due_aadhar",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"delay_reason":value,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_agree_pay_2_pre_due_aadhar",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"delay_reason":value,"stop_conversation": "TRUE"}
        elif value == "FALSE":
            if link_status == "YES":
                dispatcher.utter_template("utter_non_financial_reason_pre_due_aadhar",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="delay reason",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"delay_reason":value,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_non_financial_reason_2_pre_due_aadhar",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="delay reason",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"delay_reason":value,"stop_conversation": "TRUE"}
        elif value == "inform_call_later":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            if entities:
                if length>1:
                    time = entities[1]["value"]
                    date = entities[0]["value"]
                    callback_time = date+" "+time
                    print("The value of time",time)
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"delay_reason":value,"stop_conversation": "TRUE"}
                elif length==1:
                    date = entities[0]["value"]
                    callback_time = date
                    dispatcher.utter_template("utter_call_back_time_given_pre_due_aadhar",tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    return {"delay_reason":value,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_call_back_time_not_given_pre_due_aadhar",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"delay_reason":value,"stop_conversation": "TRUE"}
    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any]
    ) -> List[EventType]:
        return [FollowupAction("action_listen"), AllSlotsReset()]
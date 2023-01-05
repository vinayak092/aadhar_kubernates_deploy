# from dataclasses import dataclass
from datetime import datetime
from email import utils
import time 
            
from actions.utils.common_imports import *
from actions.utils.helper import *
import handle_bulk_data
helper = Helper()

class  Aadhar_Postbounce_form(FormAction):
    def name(self):
        return "aadhar_postbounce_form"

    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        availability_status = tracker.get_slot("availability_status")
        call_back = tracker.get_slot("call_back")
        name_confirmation = tracker.get_slot("name_confirmation")
        available_two = tracker.get_slot("available_two")
        payment_confirmation = tracker.get_slot("payment_confirmation")
        payment_done = tracker.get_slot("payment_done")
        payment_mode = tracker.get_slot("payment_mode")
        delay_reason = tracker.get_slot("delay_reason")
        ask_partial_payment = tracker.get_slot("ask_partial_payment")
        partial_payment_confirmation = tracker.get_slot("partial_payment_confirmation")
        ptp_payment = tracker.get_slot("ptp_payment")
        ptp_payment_two = tracker.get_slot("ptp_payment_two")
        if stop_conversation == "TRUE":
            return []
        if ptp_payment_two == "ask_partial_payment":
            return ["ask_partial_payment"]
        if ptp_payment == "ptp_payment_two":
            return ["ptp_payment_two"]
        if ptp_payment == "ask_partial_payment":
            return ["ask_partial_payment"]
        if ptp_payment == "payment_done":
            return ["payment_done"]
        if ask_partial_payment == "partial_payment_confirmation":
            return ["partial_payment_confirmation"]
        if ask_partial_payment == "payment_done":
            return ["payment_done"]
        if delay_reason== "ask_partial_payment":
            return ["ask_partial_payment"]
        if delay_reason== "ptp_payment":
            return ["ptp_payment"]
        if delay_reason== "payment_done":
            return ["payment_done"]
        if payment_mode == "ask_partial_payment":
            return ["ask_partial_payment"]
        if payment_mode == "payment_done":
            return ["payment_done"]
        if payment_confirmation == "payment_mode":
            return ["payment_mode"]
        if payment_confirmation == "delay_reason":
            return ["delay_reason"]
        if payment_confirmation == "ask_partial_payment":
            return ["ask_partial_payment"]
        if payment_confirmation== "payment_done":
            return ["payment_done"]
        if name_confirmation== "available_two":
            return ["available_two"]
        if availability_status== "call_back":
            return ["call_back"]
        if availability_status== "name_confirmation":
            return ["name_confirmation"]
        if availability_status== "payment_confirmation":
            return ["payment_confirmation"]
        if availability_status== "payment_done":
            return ["payment_done"]
        if availability_status== "ask_partial_payment":
            return ["ask_partial_payment"]
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
                self.from_intent(intent = "inform_wrong_info", value="wrong_number"),
                self.from_intent(intent = "wrong_number", value="wrong_number"),
                self.from_intent(intent = "inform_payment_done", value="inform_payment_done"),
                self.from_intent(intent = "third_party_contact",value="third_party_contact"),
                self.from_intent(intent = "disagree_to_proceed",value ="inform_call_later"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),
            ],
            "call_back": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "disagree_to_proceed",value ="TRUE"),
                self.from_intent(intent = "inform_call_later",value = "TRUE"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),
            ],
            "name_confirmation": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "disagree_to_proceed",value ="FALSE"),
                self.from_intent(intent = "inform_call_later",value = "FALSE"),
                self.from_intent(intent = "deny",value = "FALSE"),
                self.from_intent(intent = "third_party_contact",value="third_party_contact"),
                self.from_intent(intent = "inform_wrong_info",value="third_party_contact"),
                self.from_intent(intent = "wrong_number", value="wrong_number"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),
                
            ],
            "available_two": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_pay",value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "disagree_to_proceed",value ="TRUE"),
                self.from_intent(intent = "inform_call_later",value = "TRUE"),
                self.from_intent(intent = "deny",value = "TRUE"),
                self.from_intent(intent = "wrong_number", value="TRUE"),
                self.from_intent(intent = "third_party_contact",value="third_party_contact"),
                self.from_intent(intent = "inform_wrong_info",value="third_party_contact"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),  
            ],
            
             "payment_confirmation": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "agree_to_pay",value="TRUE"),
                self.from_intent(intent = "inform_payment_done", value="inform_payment_done"),
                self.from_intent(intent = "disagree_to_proceed",value ="inform_call_later"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),
                self.from_intent(intent = "insufficient_funds",value = "FALSE"),
                self.from_intent(intent = "deny",value = "FALSE"),
                self.from_intent(intent = "disagree_to_proceed",value ="FALSE"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),   
            ],
             "payment_done": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "disagree_to_proceed",value ="TRUE"),
                self.from_intent(intent = "inform_call_later",value = "TRUE"),
                self.from_intent(intent = "deny",value = "TRUE"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),    
            ],
             "payment_mode": [
                self.from_intent(intent = "inform_payment_done",value ="inform_payment_done"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),
                self.from_intent(intent = "deny",value = "inform_call_later"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),    
            ],
             "delay_reason": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "agree_to_pay",value="TRUE"),
                self.from_intent(intent = "deny",value ="FALSE"),
                self.from_intent(intent = "disagree_to_proceed",value ="FALSE"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),    
            ],
             "ask_partial_payment": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "inform_call_later",value = "inform_call_later"),
                self.from_intent(intent = "deny",value = "FALSE"),
                self.from_intent(intent = "disagree_to_proceed",value ="FALSE"),   
            ],
             "partial_payment_confirmation": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),   
            ],
             "ptp_payment": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "deny",value = "FALSE"),
                self.from_intent(intent = "disagree_to_proceed",value ="FALSE"), 
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),
            ],
             "ptp_payment_two": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "ask", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed",value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="pay_via_online"),
                self.from_intent(intent = "pay_via_branch", value="pay_via_branch"),
                self.from_intent(intent = "pay_via_executive", value="pay_via_executive"),
                self.from_intent(intent = "pay_via_cash",value = "pay_via_executive"),
                self.from_intent(intent = "pay_via_store",value = "pay_via_branch"),
                self.from_intent(intent = "ask_payment_link",value = "pay_via_online"),   
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
        for slot in self.required_slots(tracker):
            trail_count = tracker.get_slot("trail_count")
            if self._should_request_slot(tracker,slot):
                total_emi_amount = tracker.get_slot("total_emi_amount")
                due_date = tracker.get_slot("due_date")
                sheet_name = tracker.get_slot("sheet_name")
                emi_flow = tracker.get_slot("emi_flow")
                loan_id = tracker.get_slot("loan_id")
                customer_name = tracker.get_slot("customer_name")
                print("customer_name**************************",customer_name)
                # print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
                if slot == "availability_status":
                    print("inside availability_status",trail_count)
                    if trail_count is None:
                        trail_count = 0
                        dispatcher.utter_template("utter_greet_PB",tracker,customer_name=customer_name)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="initial_message",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_greet_PB_trim",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="initial_message",emi_flow=emi_flow)
                if slot == "call_back":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_not_available_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ub",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_not_available_PB_trim",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ub",emi_flow=emi_flow)

                if slot == "name_confirmation":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_Third_party_PB", tracker,customer_name=customer_name)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="NRPC",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_not_available_PB_trim",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="NRPC",emi_flow=emi_flow)
                if slot == "available_two":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_customer_not_available_PB", tracker,customer_name=customer_name)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ub",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_customer_not_available_PB",tracker,customer_name=customer_name)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ub",emi_flow=emi_flow)
                if slot == "payment_confirmation":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_greet_yes_PB", tracker,total_emi_amount=total_emi_amount)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="PIC",emi_flow=emi_flow)
                    else: 
                        dispatcher.utter_template("utter_greet_yes_PB",tracker,total_emi_amount=total_emi_amount)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="PIC",emi_flow=emi_flow)
                if slot == "payment_done":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_ask_payment_method_PB", tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Paid",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_ask_payment_method_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Paid",emi_flow=emi_flow)
                if slot == "payment_mode":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_agree_to_pay_PB", tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ATP",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_agree_to_pay_PB_trim",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ATP",emi_flow=emi_flow)
                if slot == "delay_reason":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_refuse_to_pay_PB", tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="RTP",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_refuse_to_pay_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="RTP",emi_flow=emi_flow)
                if slot == "ask_partial_payment":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_financial_reason_PB", tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="delay_reason",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_financial_reason_PB_trim",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="delay_reason",emi_flow=emi_flow)
                if slot == "partial_payment_confirmation":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_Partial_Payment _PB", tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="PPA",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_Partial_Payment _PB_trim",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="PPA",emi_flow=emi_flow)
                if slot == "ptp_payment":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_non_financial_reason_PB", tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="delay_reason",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_non_financial_reason_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="delay_reason",emi_flow=emi_flow)
                if slot == "ptp_payment_two":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_PTP_greater_5_PB", tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ub",emi_flow=emi_flow)
                    else:
                        dispatcher.utter_template("utter_PTP_greater_5_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ub",emi_flow=emi_flow)
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE": 
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="ATP",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"availability_status":"payment_confirmation","trail_count":None}
        if value ==  "FALSE": 
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="NRPC",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"availability_status":"name_confirmation","trail_count":None}
        elif value ==  "wrong_number": 
            dispatcher.utter_template("utter_wrong_number_PB", tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="NRPC",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"availability_status": value,"trail_count":None}
        elif value ==  "inform_payment_done":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="Paid",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"availability_status":"payment_done","trail_count":None}
        elif value == "inform_call_later":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="UB",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"availability_status":"call_back","trail_count":None}
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"availability_status": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"availability_status": value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"availability_status": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"availability_status":None}

    @staticmethod
    def validate_call_back(
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value == "TRUE":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            today_date=datetime.datetime.now().date()
            today_date=str(today_date)
            print("The value of entity length",len(entities))
            if entities:
                for entity in entities:
                    if entity.get("entity",None) == "time" and entity.get("entity", None) == "date":
                        time = entities[1]["value"]
                        date = entities[0]["value"]
                        callback_time = date+ " " +time
                        dispatcher.utter_template("utter_call _back_before_due_date_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"call_back":value,"trail_count":None,"stop_conversation": "TRUE"}
                    if entity.get("entity",None) == "time":
                        time=entities[1]["value"]
                        callback_time = today_date +" "+time
                        dispatcher.utter_template("utter_call _back_before_due_date_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"call_back":value,"trail_count":None,"stop_conversation": "TRUE"}
                    # elif entity.get("entity",None) == "date":
                    #     date = entities[0]["value"]
                    #     callback_time=date+" "+"10:00"
                    #     dispatcher.utter_template("utter_call _back_before_due_date_PB",tracker)
                    #     send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                    #     return {"call_back":value,"trail_count":None,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_call _back_without_due_date_PB",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=DEFAULT_FLAG,emi_flow=emi_flow)
                return {"call_back":value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"call_back": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"call_back": value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"call_back": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"call_back":None}


    @staticmethod
    def validate_name_confirmation(
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "inform_call_later":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="UB",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"name_confirmation":"call_back","trail_count":None}
        elif value ==  "TRUE":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="initial_message",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"name_confirmation":"availability_status","trail_count":None,"availability_status":None}     
        elif value == "wrong_number":
            dispatcher.utter_template("utter_wrong_number_PB", tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="NRPC",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"name_confirmation":value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "third_party_contact":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="NRPC",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"name_confirmation":"available_two","trail_count":None}
        elif value == "FALSE":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="NRPC",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"name_confirmation":"available_two","trail_count":None}
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"name_confirmation": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"name_confirmation": value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"name_confirmation": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"name_confirmation":None}

    @staticmethod
    def validate_available_two(
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value == "TRUE":
            entities = tracker.latest_message["entities"]
            print("The value of entity length",len(entities))
            if entities:
                for entity in entities:
                    if entity.get("entity",None) == "time" and entity.get("entity", None) == "date":
                        time = entities[1]["value"]
                        date = entities[0]["value"]
                        callback_time = date+ " " +time
                        dispatcher.utter_template("utter_call_back_with_time_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"available_two":value,"trail_count":None,"stop_conversation": "TRUE"}
                    elif entity.get("entity",None) == "time":
                        time=entities[1]["value"]
                        callback_time = time
                        dispatcher.utter_template("utter_call_back_with_time_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"available_two":value,"trail_count":None,"stop_conversation": "TRUE"}
                    elif entity.get("entity",None) == "date":
                        date = entities[0]["value"]
                        callback_time=date+" "+"10:00"
                        dispatcher.utter_template("utter_call_back_with_time_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"available_two":value,"trail_count":None,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_call_back_without_time_PB",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=DEFAULT_FLAG,emi_flow=emi_flow)
                return {"available_two":value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "third_party_contact":
            dispatcher.utter_template("utter_call_back_without_time_PB",tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="NRPC",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"available_two":value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"available_two": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"available_two": value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"available_two": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"available_two":None}

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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount: , due_date: ,sheet_name: ,emi_flow: ,loan_id: ,customer_name: ")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            entities = tracker.latest_message["entities"]
            time_now = datetime.datetime.now()
            time_now=str(time_now)
            time_now=time_now[:10]
            # time_now=int(time_now)
            print("time_now....: ",time_now)
            intent = tracker.latest_message.get("intent").get("name")
            if entities:
                if intent in date_check_intents:
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given_date >>>>>>>>>>>>>>>>>>>>", given_date)
                            given_date = given_date.strftime("%d-%m-%Y")
                            print("given_date >>>>", given_date)
                            today_date = datetime.datetime.now()
                            today_date = today_date.strftime("%d-%m-%Y")
                            # given_date=(given_date)
                            # given_date=given_date[:10]
                            # given_date=int(given_date)
                            # print("given date", given_date)
                            # print(type(time_now),type(given_date))
                            d1 = datetime.datetime.strptime(given_date, "%d-%m-%Y")
                            d2 =  datetime.datetime.strptime(today_date, "%d-%m-%Y")
                            ptp_days = d1-d2
                            ptp_days = ptp_days.days
                            # ptp_days = given_date - today_date
                            # print("ptp_days ....:",int(ptp_days))
                            # ptp_days=ptp_days.days
                            if ptp_days <=0:
                                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="APTP",
                                                                flag=DEFAULT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                                return {"payment_confirmation":"payment_mode","trail_count":None}
                            elif ptp_days >=1 and ptp_days<30:
                                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                user_message=user_message,
                                                                disposition_id="FPTP",
                                                                flag=DEFAULT_FLAG, ptp_date=given_date,emi_flow=emi_flow)
                                return {"payment_confirmation": "delay_reason", "trail_count": None}
                            elif ptp_days>=30:
                                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                user_message=user_message,
                                                                disposition_id="DPTP",
                                                                flag=DEFAULT_FLAG, ptp_date=given_date,emi_flow=emi_flow)
                                
                                return {"payment_confirmation": "delay_reason", "trail_count": None}
            else:
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="RTP",
                                                                    flag=DEFAULT_FLAG,emi_flow=emi_flow)
                return {"payment_confirmation":"payment_mode","trail_count":None}
            # entities = tracker.latest_message["entities"]
            # length = len(entities)
            # if entities:
            #     for entity in entities:
            #         if length>1:
            #             given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
            #             given_date = given_date.strftime("%d-%m-%Y")
            #             d1 = datetime.datetime.now()
            #             d1 = d1.strftime("%d/%m/%Y")
            #             d2 = datetime.datetime.strptime(given_date, "%d-%m-%Y")
            #             val = d2-d1
            #             days = val.days
            #             if days<=0:
            #                 time = entities[1]["value"]
            #                 date = entities[0]["value"]
            #                 callback_time = date+" "+time
            #                 print("The value of time",time)
            #                 send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
            #                             disposition_id="SDP",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            #                 return {"payment_confirmation":"payment_mode","trail_count":None}
            #             else:
            #                 send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="PIC",flag=DEFAULT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
            #                 return {"payment_confirmation":"delay_reason","trail_count":None}
            #         else:
            #             now = datetime.datetime.now()
            #             date = entities[0]["value"]
            #             callback_time = date+" "+"10:00"
            #             current_time = now.strftime("%H:%M")
            #             # val = get_time(current_time)
            #             given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
            #             given_date = given_date.strftime("%d-%m-%Y")
            #             due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y")
            #             due_date = due_date.strftime("%d-%m-%Y")
            #             d1 = datetime.datetime.strptime(due_date, "%d-%m-%Y")
            #             d2 = datetime.datetime.strptime(given_date, "%d-%m-%Y")
            #             val = d2-d1
            #             days = val.days
            #             if days<=0:
            #                 send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="SDP",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            #                 return {"payment_confirmation":"payment_mode","trail_count":None}
            #             else:
            #                 send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="PIC",flag=DEFAULT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
            #                 return {"payment_confirmation":"delay_reason","trail_count":None}
            # else:
            #     send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="ATP",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            #     return {"payment_confirmation":"payment_mode","trail_count":None}

        elif value == "FALSE":
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation":"delay_reason","trail_count":None}
        elif value == "inform_payment_done":
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="Paid",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation":"payment_done","trail_count":None}
        elif value == "inform_call_later":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            print("The value of entity length",len(entities))
            if entities:
                for entity in entities:
                    if entity.get("entity",None) == "time" and entity.get("entity", None) == "date":
                        time = entities[1]["value"]
                        date = entities[0]["value"]
                        callback_time = date+ " " +time
                        dispatcher.utter_template("utter_call _back_before_due_date_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"payment_confirmation":value,"trail_count":None,"stop_conversation": "TRUE"}
                    elif entity.get("entity",None) == "time":
                        time=entities[1]["value"]
                        callback_time = time
                        dispatcher.utter_template("utter_call _back_before_due_date_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"payment_confirmation":value,"trail_count":None,"stop_conversation": "TRUE"}
                    elif entity.get("entity",None) == "date":
                        date = entities[0]["value"]
                        callback_time=date+" "+"10:00"
                        dispatcher.utter_template("utter_call _back_before_due_date_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"payment_confirmation":value,"trail_count":None,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_call _back_without_due_date_PB",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=DEFAULT_FLAG,emi_flow=emi_flow)
                return {"payment_confirmation":value,"trail_count":None,"stop_conversation": "TRUE"}
            
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation": value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_confirmation": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"payment_confirmation":None}

    @staticmethod
    def validate_payment_done(
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            dispatcher.utter_template("utter_paid_PB",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="Paid",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_done": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"payment_done":None}
            
   

    @staticmethod
    def validate_payment_mode(
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "inform_payment_done":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="Paid",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"payment_mode":"payment_done","trail_count":None}

        
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_mode": value,"trail_count":None, "stop_conversation": "TRUE"}

        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_mode": value,"trail_count":None,"stop_conversation": "TRUE"}

        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"payment_mode": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"payment_mode":None}
    
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="ATP",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"delay_reason":"payment_mode","trail_count":None}

        elif value == "inform_call_later":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            date_today= datetime.datetime.now().date()
            print("The value of entity length",len(entities))
            if entities:
                for entity in entities:
                    if entity.get("entity",None) == "time" and entity.get("entity", None) == "date":
                        time = entities[1]["value"]
                        date = entities[0]["value"]
                        callback_time = date+ " " +time
                        dispatcher.utter_template("utter_call _back_before_due_date_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"delay_reason":value,"trail_count":None,"stop_conversation": "TRUE"}
                    elif entity.get("entity",None) == "time":
                        time=entities[1]["value"]
                        callback_time = date_today+" "+time
                        dispatcher.utter_template("utter_call _back_before_due_date_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"delay_reason":value,"trail_count":None,"stop_conversation": "TRUE"}
                    elif entity.get("entity",None) == "date":
                        date = entities[0]["value"]
                        callback_time=date+" "+"10:00"
                        dispatcher.utter_template("utter_call _back_before_due_date_PB",tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=TIMEOUT_FLAG,emi_flow=emi_flow,callback_time = callback_time)
                        return {"delay_reason":value,"trail_count":None,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_call _back_without_due_date_PB",tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,disposition_id="UB",flag=DEFAULT_FLAG,emi_flow=emi_flow)
                return {"delay_reason":value,"trail_count":None,"stop_conversation": "TRUE"}
        
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"delay_reason": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"delay_reason": value,"trail_count":None,"stop_conversation": "TRUE"}
            
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"delay_reason": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"delay_reason":None}

    @staticmethod
    def validate_ask_partial_payment(
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="PPA",flag=DEFAULT_FLAG,emi_flow=emi_flow)
            return {"ask_partial_payment":"partial_payment_confirmation","trail_count":None}

        elif value == "FALSE":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            if entities:
                for entity in entities:
                    if entity.get("entity",None) == "number":
                        number = entities[0]["value"]
                        accepted_amount=0.2*total_emi_amount
                        if number>accepted_amount:
                            dispatcher.utter_template("utter_amount_more_20_PB",tracker)
                            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="PPA",emi_flow=emi_flow)
                            return {"ask_partial_payment": value,"trail_count":None,"stop_conversation": "TRUE"}
                        else:
                            dispatcher.utter_template("utter_amount_less_20_PB",tracker)
                            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="PPA",emi_flow=emi_flow)
                            return {"ask_partial_payment": value,"trail_count":None,"stop_conversation": "TRUE"}

            else:
                dispatcher.utter_template("utter_amount_less_20_PB",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="PPA",emi_flow=emi_flow)
                return {"ask_partial_payment": value,"trail_count":None,"stop_conversation": "TRUE"}
    
    
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ask_partial_payment": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ask_partial_payment": value,"trail_count":None,"stop_conversation": "TRUE"}
            
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ask_partial_payment": value,"trail_count":None, "stop_conversation": "TRUE"}

        return{"ask_partial_payment":None}

    @staticmethod
    def validate_partial_payment_confirmation(
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            entities = tracker.latest_message["entities"]
            length = len(entities)
            if entities:
                for entity in entities:
                    if entity.get("entity",None) == "number":
                        number = entities[0]["value"]
                        accepted_amount=0.2*total_emi_amount
                        if number>accepted_amount:
                            dispatcher.utter_template("utter_amount_more_20_PB",tracker)
                            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="PPA",emi_flow=emi_flow)
                            return {"partial_payment_confirmation": value,"trail_count":None,"stop_conversation": "TRUE"}
                        else:
                            dispatcher.utter_template("utter_amount_less_20_PB",tracker)
                            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="PPA",emi_flow=emi_flow)
                            return {"partial_payment_confirmation": value,"trail_count":None,"stop_conversation": "TRUE"}

            else:
                dispatcher.utter_template("utter_amount_less_20_PB",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="PPA",emi_flow=emi_flow)
                return {"partial_payment_confirmation": value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"partial_payment_confirmation": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"partial_payment_confirmation": value,"trail_count":None,"stop_conversation": "TRUE"}
            
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"partial_payment_confirmation": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"partial_payment_confirmation":None}
        

    @staticmethod
    def validate_ptp_payment(
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            entities = tracker.latest_message["entities"]
            now = datetime.datetime.now()
            intent = tracker.latest_message.get("intent").get("name")
            if entities:
                if intent in date_check_intents:
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                due_date=datetime.datetime.strptime(due_date,"%d-%m-%Y").date()
                                ptp_days = given_date.date() - datetime.datetime.now().date()
                                print("no of days", ptp_days)
                                if ptp_days.days <5:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_PTP_Lesser_5_PB",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                                    return {"ptp_payment":value,"trail_count":None,"stop_conversation": "TRUE"}
                                elif ptp_days.days>5 and ptp_days.days.days<30:
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="FPTP",
                                                                    flag=DEFAULT_FLAG, ptp_date=given_date,emi_flow=emi_flow)
                                    return {"ptp_payment": "ptp_payment_two", "trail_count": None}
                                elif ptp_days.days>=30:
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="DPTP",
                                                                    flag=DEFAULT_FLAG, ptp_date=given_date,emi_flow=emi_flow)
                                    
                                    return {"ptp_payment": "ptp_payment_two", "trail_count": None}
            else:
                dispatcher.utter_template("utter_PTP_no_date_PB",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="FPTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"ptp_payment":value,"trail_count":None,"stop_conversation": "TRUE"}
            
        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ptp_payment": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ptp_payment": value,"trail_count":None,"stop_conversation": "TRUE"}
            
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ptp_payment": value,"trail_count":None, "stop_conversation": "TRUE"}
        return{"ptp_payment":None}

    @staticmethod        
    def validate_ptp_payment_two(
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
        print(total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,"total_emi_amount,due_date,sheet_name,emi_flow")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            entities = tracker.latest_message["entities"]
            now = datetime.datetime.now()
            intent = tracker.latest_message.get("intent").get("name")
            if entities:
                if intent in date_check_intents:
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                due_date=datetime.datetime.strptime(due_date,"%d-%m-%Y").date()
                                ptp_days = given_date.date() - datetime.datetime.now().date()
                                print("no of days", ptp_days)
                                if ptp_days.days <5:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_PTP_Lesser_5_PB",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow=emi_flow,ptp_date=given_date)
                                    return {"ptp_payment_two":value,"trail_count":None,"stop_conversation": "TRUE"}
                                elif ptp_days.days>5 and ptp_days.days.days<30:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_PTP_no_date_PB",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="FPTP",
                                                                    flag=TIMEOUT_FLAG, ptp_date=given_date,emi_flow=emi_flow)
                                    return {"ptp_payment_two": value, "trail_count": None,"stop_conversation": "TRUE"}
                                elif ptp_days.days>=30:
                                    dispatcher.utter_template("utter_PTP_no_date_PB",tracker)
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="DPTP",
                                                                    flag=TIMEOUT_FLAG, ptp_date=given_date,emi_flow=emi_flow)
                                    
                                    return {"ptp_payment_two": value, "trail_count": None,"stop_conversation": "TRUE"}
            else:
                dispatcher.utter_template("utter_PTP_no_date_PB",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="FPTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow=emi_flow)
                return {"ptp_payment_two":value,"trail_count":None,"stop_conversation": "TRUE"}


        elif value == "pay_via_online":
            dispatcher.utter_template("utter_pay_online_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ptp_payment_two": value,"trail_count":None, "stop_conversation": "TRUE"}
        elif value == "pay_via_branch":
            dispatcher.utter_template("utter_pay_branch_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ptp_payment_two": value,"trail_count":None,"stop_conversation": "TRUE"}
            
        elif value == "pay_via_executive":
            dispatcher.utter_template("utter_pay_executive_PB", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="ATP",
                                               flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return {"ptp_payment_two": value,"trail_count":None, "stop_conversation": "TRUE"}

        return{"ptp_payment_two":None}

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any]
    ) -> List[EventType]:
        return [FollowupAction("action_listen"), AllSlotsReset()] 
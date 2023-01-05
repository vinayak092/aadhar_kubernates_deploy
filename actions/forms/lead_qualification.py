import datetime
from email import utils
from multiprocessing.sharedctypes import Value
import time 

from actions.utils.common_imports import *
from actions.utils.helper import *

helper = Helper()

class LeadQualification(FormAction):
    def name(self):
        return "lead_qualificationform"

    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        payment_confirmation = tracker.get_slot("payment_confirmation")
        availability_status = tracker.get_slot("availability_status")
        ask_delay_reason = tracker.get_slot("ask_delay_reason")
        ask_monthly_salary = tracker.get_slot("ask_monthly_salary")
        receive_salary = tracker.get_slot("receive_salary")
        if stop_conversation == "TRUE":
            return []
        if payment_confirmation == "ask_delay_reason":
            return ["ask_delay_reason"]
        if availability_status == "ask_delay_reason":
            return ["ask_delay_reason"]
        if receive_salary == "ask_bank_statement":
            return["ask_bank_statement"]
        if ask_monthly_salary  == "receive_salary":
            return ["receive_salary"]
        if payment_confirmation == "ask_monthly_salary":
            return ["ask_monthly_salary"]
        if availability_status == "payment_confirmation":
            return ["payment_confirmation"]
        if availability_status == "ask_credit_limit":
            return ["ask_credit_limit"]
        if availability_status == "ask_interest_rate":
            return ["ask_interest_rate"]
        return ["availability_status"]

    def get_emi_date_amount(self,value=None):
        return[
            self.from_intent(intent = "ask_emi_amount", value="ask_emi_amount"),
            self.from_intent(intent = "ask_emi_due_date", value="ask_emi_due_date"),
        ]
    def get_delay_reason(self,value=None):
        return [
            self.from_intent(intent="business_loss", value=value),
            self.from_intent(intent="insufficient_funds", value=value),
            # self.from_intent(intent="job_loss", value=value),
            # self.from_intent(intent="foreclosing_through_own_funds", value=value),
            self.from_intent(intent="branch_issue", value=value),
            # self.from_intent(intent="account_not_working", value=value),
            # self.from_intent(intent="change_account_for_deduction", value=value),
            self.from_intent(intent="personal_issue",value=value)
        ]

    def slot_mappings(self):
        return{
            "availability_status": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="TRUE"),
                self.from_intent(intent = "inform",value = "TRUE"),
                self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_method", value="TRUE"),
                self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "disagree_to_pay", value="disagree_to_proceed"),
                self.from_intent(intent = "deny", value="disagree_to_proceed"),
                self.from_intent(intent = "disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent = "inform_wrong_info", value="inform_wrong_info"),
                self.from_intent(intent = "bye", value="bye"),
                self.from_intent(intent = "ask_interest_rate",value="ask_interest_rate"),
                self.from_intent(intent = "ask_credit_limit",value = "ask_credit_limit"),
            ] + self.get_delay_reason(value="decline_reason"),
            "payment_confirmation": [
                self.from_intent(intent = "inform_salaried",value = "TRUE"),
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "pay_via_agent", value="TRUE"),
                self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_method", value="TRUE"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
               
            ] + self.get_delay_reason(value="decline_reason"),
            "ask_interest_rate":[
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "inform_salaried",value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "pay_via_agent", value="TRUE"),
                self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_method", value="TRUE"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
            ]+ self.get_delay_reason(value="decline_reason"),
            "ask_credit_limit":[
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "inform_salaried",value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "pay_via_agent", value="TRUE"),
                self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_method", value="TRUE"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
            ]+self.get_delay_reason(value="decline_reason"),
            "receive_salary":[
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "inform_salaried",value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "pay_via_agent", value="TRUE"),
                self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_method", value="TRUE"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "salary_via_cash",value = "salary_via_cash"),
                self.from_intent(intent = "salary_via_bank_transfer",value = "salary_via_bank_transfer"),
                self.from_intent(intent = "salary_via_cheque",value = "salary_via_cheque"),
            ]+self.get_delay_reason(value="decline_reason"),
            "ask_bank_statement": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "inform_salaried",value="TRUE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "pay_via_agent", value="TRUE"),
                self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_method", value="TRUE"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
            ] + self.get_delay_reason(value="decline_reason")
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
                total_loans = get_total_loan(tracker)
                total_emi_amount,due_date,sheet_name,emi_flow = get_emi_details(tracker,total_loans)
                print(total_emi_amount,due_date,sheet_name,emi_flow,"total_emi_amount,due_date,sheet_name,emi_flow")
                if slot == "availability_status":
                    print("inside availability_status",trail_count)
                    if trail_count is None:
                        trail_count = 0
                        day_time = helper.get_daytime()
                        print("The due date value is",due_date)
                        emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
                        ptp_date = emi_date.strftime("%d %B %Y")
                        print("The value of date ",emi_date)
                        dispatcher.utter_template("utter_greet_LQ",tracker,)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="pic",emi_amount=total_emi_amount,emi_flow="due_date")
                    else:
                        emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
                        ptp_date = emi_date.strftime("%d %B %Y")
                        print("The value of date ",emi_date)
                        dispatcher.utter_template("utter_pay_today",tracker)
                        # return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        # SlotSet("timestamp", time.time())]

                if slot == "payment_confirmation":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_ask_intrest_rate_yes_LQ",tracker)
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,emi_flow="due_date")
                if slot == "ask_interest_rate":
                    if trail_count is None:
                        trail_count = 0
                        dispatcher.utter_template("utter_ask_intrest_rate_LQ", tracker)
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,emi_flow="due_date")
                if slot == "ask_credit_limit":
                    if trail_count is None:
                        trail_count = 0
                        dispatcher.utter_template("")
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,emi_flow="due_date")
                if slot == "ask_monthly_salary":
                    if trail_count is None:
                        trail_count = 0
                        dispatcher.utter_template("utter_salaried_LQ",tracker)
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,emi_flow="due_date")
                if slot == "receive_salary":
                    if trail_count is None:
                        trail_count = 0
                        dispatcher.utter_template("utter_salaried_yes_LQ",tracker)
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,emi_flow="due_date")
                if slot == "ask_bank_statement":
                    if trail_count is None:
                        trail_count  = 0
                        dispatcher.utter_template("utter_sal_cheque_LQ",tracker)
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,emi_flow="due_date")
                if slot == "ask_delay_reason":
                    dispatcher.utter_template("utter_delay_reason_due_date", tracker)
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,emi_flow="due_date")
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
        total_loans = get_total_loan(tracker)
        total_emi_amount,due_date,sheet_name,emi_flow = get_emi_details(tracker,total_loans)
        if value ==  "TRUE":
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="agree to pay",flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"availability_status":"payment_confirmation","trail_count":None,}
        if value == "disagree_to_proceed":
            dispatcher.utter_template("utter_not_available_LQ", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="disagree to proceed",flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}
        elif value == "inform_wrong_info":
            dispatcher.utter_template("utter_agent_will_connect_common", tracker)
            dispatcher.utter_template("utter_bye", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"availability_status": value, "stop_conversation": "TRUE"}
        elif value == "+1":
            dispatcher.utter_template("utter_confirm_again", tracker)
            return {"availability_status": value}
        elif value=="bye":
            dispatcher.utter_template("utter_bye_common",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="bye",emi_flow="due_date")
            return {"stop_conversation":"TRUE"}
        elif value == "ask_interest_rate":
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=DEFAULT_FLAG,emi_flow="due_date")
            return {"availability_status": "ask_interest_rate", "trail_count":None}
        return{"availability_status":None}


    @staticmethod
    def validate_ask_interest_rate(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any], 
    ):
        user_message = tracker.latest_message.get("text")
        if value == "TRUE":
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                flag=DEFAULT_FLAG,emi_flow="due_date")
            return {"ask_interest_rate": "payment_confirmation", "trail_count": None}
        elif value == "FALSE":
            dispatcher.utter_template("utter_not_available_LQ", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"ask_interest_rate":value,"stop_conversation": "TRUE"}

    @staticmethod
    def validate_ask_credit_limit(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any], 
    ):
        user_message = tracker.latest_message.get("text")
        if value == "TRUE":
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                flag=DEFAULT_FLAG,emi_flow="due_date")
            return {"ask_credit_limit": "payment_confirmation", "trail_count": None}
        elif value == "FALSE":
            dispatcher.utter_template("utter_not_available_LQ", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"ask_credit_limit":value,"stop_conversation": "TRUE"}

    @staticmethod
    def validate_payment_confirmation(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any], 
    ):
        total_loans = get_total_loan(tracker)
        total_emi_amount,due_date,sheet_name,emi_flow = get_emi_details(tracker,total_loans)
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                            flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"payment_confirmation": "ask_monthly_salary", "stop_conversation": "TRUE", "trail_count": None}
        elif value == "FALSE":
            # dispatcher.utter_template("utter_diagree_to_pay", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="rtp", flag=DEFAULT_FLAG,emi_flow="due_date")
            return {"payment_confirmation": "ask_delay_reason"}

        elif value == "decline_reason":
            dispatcher.utter_template("utter_not_accepted_reason_due_date", tracker)
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}

        elif value == "inform_wrong_info":
            dispatcher.utter_template("utter_agent_will_connect", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"payment_confirmation": value, "stop_conversation": "TRUE"}

        elif value == "inform_payment_done":
            dispatcher.utter_template("utter_already_paid_due_date",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                        disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"trail_count":None,"payment_confirmation":value,"stop_conversation":"TRUE"}

    @staticmethod
    def validate_ask_monthly_salary(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any]
    ):
        user_message = tracker.latest_message.get("text")
        if value == "TRUE":
            entities = tracker.latest_message["entities"]
            if entities:
                if intent in date_check_intents:
                    # TODO store the promise to pay date, and need to add payment link response also
                    for entity in entities:
                        if entity.get("entity", None) == "number":
                            value = entity["value"]
                            if value <= 15000:
                                dispatcher.utter_template("utter_self_employed_LQ",tracker)
                                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="due_date")
                                return {"ask_monthly_salary":value,"stop_conversation":"TRUE"}
                            else:
                                intent = tracker.latest_message.get("intent").get("name")
                                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                                                delay_reason=decline_reason_disposition_id.get(intent),
                                                                flag=DEFAULT_FLAG,emi_flow="due_date")
                                return {"ask_monthly_salary":"receive_salary","trail_count":None}
        intent = tracker.latest_message.get("intent").get("name")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
            delay_reason=decline_reason_disposition_id.get(intent),flag=DEFAULT_FLAG,emi_flow="due_date")
        return {"ask_monthly_salary":"receive_salary","trail_count":None}

    @staticmethod
    def validate_receive_salary(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any]
    ):
        user_message = tracker.latest_message.get("text")
        if value == "salary_via_cheque":
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=DEFAULT_FLAG,emi_flow="due_date")
            return {"receive_salary":"ask_bank_statement","trail_count":None}
        if value == "salary_via_bank_transfer":
            intent = tracker.latest_message("intent").get("name")
            dispatcher.utter_template("utter_sal_bank_act_LQ",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"receive_salary":value,"stop_conversation":"TRUE"}
        if value == "salary_via_cash":
            intent = tracker.latest_message("intent").get("name")
            dispatcher.utter_template("utter_sal_cash_LQ",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"receive_salary":value,"stop_conversation":"TRUE"}


    @staticmethod
    def validate_ask_bank_statement(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any]
    ):
        user_message = tracker.latest_message.get("text")
        intent = tracker.latest_message.get("intent").get("name")
        if value == "TRUE":
            dispatcher.utter_template("utter_act_st_yes_LQ",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"ask_bank_statement":value,"stop_conversation":"TRUE"}
        elif value == "FALSE":
            dispatcher.utter_template("utter_act_st_no_LQ",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"ask_bank_statement":value,"stop_conversation":"TRUE"}

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any]
    ) -> List[EventType]:
        return [FollowupAction("action_listen"), AllSlotsReset()] 
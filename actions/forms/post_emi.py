import datetime
from email import utils
import time 

from actions.utils.common_imports import *
from actions.utils.helper import *
import handle_bulk_data
helper = Helper()

class post_emi_form(FormAction):
    def name(self):
        return "post_emi_form"

    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        payment_confirmation = tracker.get_slot("payment_confirmation")
        availability_status = tracker.get_slot("availability_status")
        ask_delay_reason = tracker.get_slot("ask_delay_reason")
        if stop_conversation == "TRUE":
            return []
        if payment_confirmation == "ask_delay_reason":
            return ["ask_delay_reason"]
        if availability_status == "ask_delay_reason":
            return ["ask_delay_reason"]
        if availability_status == "payment_confirmation":
            return ["payment_confirmation"]
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
                self.from_intent(intent = "deny", value="deny"),
                self.from_intent(intent = "disagree_to_proceed", value="disagree_to_proceed"),
                self.from_intent(intent = "inform_wrong_info", value="inform_wrong_info"),
                self.from_intent(intent = "agree_to_pay", value="agree_to_pay"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "bye", value="bye"),
                # self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_method", value="TRUE"),
                self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                # self.from_intent(intent = "ask_emi_amount", value="ask_emi_amount"),
                # self.from_intent(intent = "ask_emi_due_date", value="ask_emi_due_date"),
                # self.from_intent(intent = "ask_partial_payment",value = "disagree_to_pay"),
            ] + self.get_delay_reason(value="decline_reason"),
            "payment_confirmation": [
                self.from_intent(intent = "affirm", value="TRUE"),
                self.from_intent(intent = "agree_to_proceed", value="TRUE"),
                self.from_intent(intent = "inform", value="TRUE"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                self.from_intent(intent = "agree_to_pay", value="TRUE"),
                self.from_intent(intent = "pay_via_agent", value="TRUE"),
                self.from_intent(intent = "pay_via_branch", value="TRUE"),
                self.from_intent(intent = "pay_via_online", value="TRUE"),
                self.from_intent(intent = "ask_payment_link", value="TRUE"),
                # self.from_intent(intent = "ask_payment_link", value="TRUE"),
                self.from_intent(intent = "ask_payment_method", value="TRUE"),
                # self.from_intent(intent = "ask_emi_amount", value="ask_emi_amount"),
                # self.from_intent(intent = "ask_emi_due_date", value="ask_emi_due_date"),
                # self.from_intent(intent = "ask_partial_payment",value = "disagree_to_pay"),
            ] + self.get_delay_reason(value="decline_reason"),
            "ask_delay_reason": [
                self.from_intent(intent = "affirm", value="+1"),
                self.from_intent(intent = "agree_to_proceed", value="+1"),
                self.from_intent(intent = "inform",value = "TRUE"),
                self.from_intent(intent = "agree_to_pay", value="agree_to_pay"),
                self.from_intent(intent = "deny", value="FALSE"),
                self.from_intent(intent = "disagree_to_proceed", value="FALSE"),
                self.from_intent(intent = "disagree_to_pay", value="FALSE"),
                # self.from_intent(intent = "ask_emi_amount", value="ask_emi_amount"),
                # self.from_intent(intent = "ask_emi_due_date", value="ask_emi_due_date"),
                # self.from_intent(intent = "ask_partial_payment",value = "disagree_to_pay"),
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
                data = handle_bulk_data.detect_camapin()
                if data == "yes":
                    total_loans = get_total_loan(tracker)
                    total_emi_amount,due_date,sheet_name,emi_flow,loan_id = get_emi_details(tracker,total_loans)
                else:
                    user_details=get_user_details_redis(tracker)
                    emi_flow=user_details.get("flow_type")
                    total_emi_amount = user_details.get("total_emi_amt")
                    loan_id = user_details.get("loan_id")
                    due_date = user_details.get("due_date")
                    sheet_name = user_details.get("sheet_name")
                # total_emi_amount,due_date,sheet_name,emi_flow = get_emi_details(tracker,total_loans)
                print(total_emi_amount,due_date,sheet_name,emi_flow,"total_emi_amount,due_date,sheet_name,emi_flow")
                if slot == "availability_status":
                    print("inside availability_status",trail_count)
                    if trail_count is None:
                        trail_count = 0
                        day_time = helper.get_daytime()
                        print("The due date value is",due_date)
                        # date = due_date[0].date()
                        # value = datetime.strptime(due_date[0],'%d/%m/%Y')
                        if data == "yes":
                            emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
                        else:
                            emi_date = datetime.datetime.strptime(due_date, "%d-%m-%Y")
                        # emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
                        ptp_date = emi_date.strftime("%d %B %Y")
                        print("The value of date ",emi_date)
                        # ptp_date = value.strftime("%d %B, %Y").replace(",","")
                        dispatcher.utter_template("utter_greet_a_due_date",tracker,monthly_emi = total_emi_amount,monthly_emi_date=ptp_date)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="pic",emi_amount=total_emi_amount,
                                        emi_flow="due_date")
                    else:
                        if data == "yes":
                            emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
                        else:
                            emi_date = datetime.datetime.strptime(due_date, "%d-%m-%Y")
                        # emi_date = datetime.datetime.strptime(due_date[0], "%d-%m-%Y")
                        ptp_date = emi_date.strftime("%d %B %Y")
                        print("The value of date ",emi_date)
                        dispatcher.utter_template("utter_pay_today",tracker)
                        # return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        # SlotSet("timestamp", time.time())]

                if slot == "payment_confirmation":
                    if trail_count is None:
                        trail_count=0
                        dispatcher.utter_template("utter_ptp_given_due_date",tracker)
                    else:
                        dispatcher.utter_template("utter_ptp_given_due_date",tracker)
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
        data = handle_bulk_data.detect_camapin()
        if data == "yes":
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,loan_id = get_emi_details(tracker,total_loans)
        else:
            user_details=get_user_details_redis(tracker)
            emi_flow=user_details.get("flow_type")
            monthly_emi = user_details.get("total_emi_amt")
            loan_id = user_details.get("loan_id")
            due_date = user_details.get("due_date")
            sheet_name = user_details.get("sheet_name")
        if value ==  "TRUE":
            dispatcher.utter_template("utter_agree_to_pay_due_date",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="agree to pay",flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}

        if value == "disagree_to_proceed":
            user_details = get_user_details(tracker)
            monthly_emi = user_details.get("total_emi_amt")
            monthly_emi_date = user_details.get("Due date")
            # user_details = get_user_details(tracker)
            # monthly_emi = user_details.get("total_emi_amt")
            # monthly_emi_date = user_details.get("Due date")
            # dispatcher.utter_template("utter_not_available_to_talk",tracker,monthly_emi = monthly_emi,monthly_emi_date = monthly_emi_date)
            dispatcher.utter_template("utter_not_available_to_talk", tracker,monthly_emi = monthly_emi)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="disagree to proceed",flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}

        if value == "FALSE":
            print("Coming this disagree to pay1")
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,user_message=user_message,
                disposition_id="rtp",flag=DEFAULT_FLAG,emi_flow="due_date")
            return {"availability_status": "payment_confirmation", "trail_count": None}

        elif value == "deny":
            # dispatcher.utter_template("utter_diagree_to_pay",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, 
                    user_message=user_message,disposition_id="deny",flag=DEFAULT_FLAG,emi_flow="due_date")
            return {"availability_status": "payment_confirmation", "trail_count": None}

        elif value == "agree_to_pay" or value =="inform":
            user_message = tracker.latest_message.get("text")
            entities = tracker.latest_message["entities"]
            now = datetime.datetime.now()
            intent = tracker.latest_message.get("intent").get("name")
            if entities:
                if intent in date_check_intents:
                    # TODO store the promise to pay date, and need to add payment link response also
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                if data == "yes":
                                    due_date=datetime.datetime.strptime(due_date[0],"%d-%m-%Y").date()
                                else:
                                    due_date=datetime.datetime.strptime(due_date,"%d-%m-%Y").date()
                                no_of_days = given_date.date() - datetime.datetime.now().date()
                                # print("no of days", no_of_days)
                                # if no_of_days.days:
                                #     return {"payment_confirmation": "ask_partial_payment", "trail_count": None}
                                if given_date.date()==due_date:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_agree_to_pay_due_date",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow="due_date",ptp_date=given_date)
                                    return {"availability_status":value,"trail_count":None,"stop_conversation": "TRUE"}
                                elif no_of_days.days>=30 and no_of_days.days<60:
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="FPTP",
                                                                    flag=DEFAULT_FLAG, ptp_date=given_date,emi_flow=emi_flow)
                                    return {"availability_status": "payment_confirmation", "trail_count": None}
                                elif no_of_days.days>=60:
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                                    user_message=user_message,
                                                                    disposition_id="DPTP",
                                                                    flag=DEFAULT_FLAG, ptp_date=given_date,emi_flow=emi_flow)
                                    
                                    return {"availability_status": "payment_confirmation", "trail_count": None}
                                else:
                                    given_date = given_date.strftime("%d %B %Y")
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="PTP", flag=DEFAULT_FLAG,emi_flow="due_date",ptp_date=given_date)
                                    return {"availability_status": "payment_confirmation", "trail_count": None}
            else:
                dispatcher.utter_template("utter_agree_to_pay_due_date",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="agree to pay",
                                                                    flag=TIMEOUT_FLAG,emi_flow="due_date",)
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
        elif value == "decline_reason":
            dispatcher.utter_template("utter_not_accepted_reason_due_date", tracker)
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"availability_status": value, "stop_conversation": "TRUE"}
        elif value=="bye":
            dispatcher.utter_template("utter_bye_common",tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=TIMEOUT_FLAG,disposition_id="bye",emi_flow="due_date")
            return {"stop_conversation":"TRUE"}
        return{"availability_status":None}

    @staticmethod
    def validate_payment_confirmation(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any], 
    ):
        data = handle_bulk_data.detect_camapin()
        if data == "yes":
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,loan_id = get_emi_details(tracker,total_loans)
        else:
            user_details=get_user_details_redis(tracker)
            emi_flow=user_details.get("flow_type")
            monthly_emi = user_details.get("total_emi_amt")
            loan_id = user_details.get("loan_id")
            due_date = user_details.get("due_date")
            sheet_name = user_details.get("sheet_name")
        user_message = tracker.latest_message.get("text")
        if value ==  "TRUE":
            entities = tracker.latest_message["entities"]
            now = datetime.datetime.now()
            intent = tracker.latest_message.get("intent").get("name")
            if entities:
                if intent in date_check_intents:
                    # TODO store the promise to pay date, and need to add payment link response also
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                if data == "yes":
                                    due_date=datetime.datetime.strptime(due_date[0],"%d-%m-%Y").date()
                                else:
                                    due_date=datetime.datetime.strptime(due_date,"%d-%m-%Y").date()
                                # print("no of days", no_of_days)
                                # if no_of_days.days:
                                #     return {"payment_confirmation": "ask_partial_payment", "trail_count": None}
                                if given_date.date()==due_date:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_agree_to_pay_due_date",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow="due_date",ptp_date=given_date)
                                    return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}
                                else:
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="PTP", flag=DEFAULT_FLAG,emi_flow="due_date")
                                    return {"payment_confirmation": "ask_delay_reason"}
            else:
                dispatcher.utter_template("utter_agree_to_pay_due_date",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="agree to pay",
                                                                    flag=TIMEOUT_FLAG,emi_flow="due_date",)
                return {"payment_confirmation": value, "stop_conversation": "TRUE", "trail_count": None}
                
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
    def validate_ask_delay_reason(
        value : Text,
        dispatcher : CollectingDispatcher,
        tracker : Tracker,
        domain : Dict[Text,Any]
    ):
        data = handle_bulk_data.detect_camapin()
        if data == "yes":
            total_loans = get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,loan_id = get_emi_details(tracker,total_loans)
        else:
            user_details=get_user_details_redis(tracker)
            emi_flow=user_details.get("flow_type")
            monthly_emi = user_details.get("total_emi_amt")
            loan_id = user_details.get("loan_id")
            due_date = user_details.get("due_date")
            sheet_name = user_details.get("sheet_name")
        user_message = tracker.latest_message.get("text")
        if value  == "FALSE":
            dispatcher.utter_template("utter_not_accepted_reason_due_date",tracker)
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="RTP",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"ask_delay_reason":value,"stop_conversation":"TRUE"}
        elif value == "agree_to_pay":
            entities = tracker.latest_message["entities"]
            now = datetime.datetime.now()
            intent = tracker.latest_message.get("intent").get("name")
            if entities:
                if intent in date_check_intents:
                    # TODO store the promise to pay date, and need to add payment link response also
                    for entity in entities:
                        if entity.get("entity", None) == "date":
                            given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                            print("given date", given_date)
                            if given_date:
                                if data == "yes":
                                    due_date=datetime.datetime.strptime(due_date[0],"%d-%m-%Y").date()
                                else:
                                    due_date=datetime.datetime.strptime(due_date,"%d-%m-%Y").date()
                                # print("no of days", no_of_days)
                                # if no_of_days.days:
                                #     return {"payment_confirmation": "ask_partial_payment", "trail_count": None}
                                if given_date.date()==due_date:
                                    given_date = given_date.strftime("%d %B %Y")
                                    dispatcher.utter_template("utter_agree_to_pay_due_date",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow="due_date",ptp_date=given_date)
                                    return {"stop_conversation": "TRUE", "trail_count": None}
                                else:
                                    dispatcher.utter_template("utter_not_accepted_reason_due_date",tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="RTP", flag=TIMEOUT_FLAG,emi_flow="due_date")
                                    return {"stop_conversation": "TRUE", "trail_count": None}
            else:
                dispatcher.utter_template("utter_agree_to_pay_due_date",tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message=user_message,disposition_id="PTP",
                                                                    flag=TIMEOUT_FLAG,emi_flow="due_date",)
                return {"stop_conversation": "TRUE", "trail_count": None}
        elif value == "decline_reason":
            dispatcher.utter_template("utter_not_accepted_reason_due_date", tracker)
            # dispatcher.utter_template("utter_bye",tracker)
            user_message = tracker.latest_message.get("text")
            intent = tracker.latest_message.get("intent").get("name")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,disposition_id="delay_reason",
                                               delay_reason=decline_reason_disposition_id.get(intent),
                                               flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"ask_delay_reason": value, "stop_conversation": "TRUE"}  
        elif value == "+1":
            dispatcher.utter_template("utter_apology", tracker)
            dispatcher.utter_template("utter_confirm_again", tracker)
            return {"ask_delay_reason": None, "trail_count": get_trail_count(tracker)}
        elif value == "+2":
            dispatcher.utter_template("utter_send_payment_link", tracker)
            dispatcher.utter_template("utter_thank_you", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="PTP", flag=TIMEOUT_FLAG,emi_flow="due_date",)
            return {"trail_count": None, "ask_delay_reason": value,"stop_conversation": "TRUE"}
        elif value == "inform_payment_done":
            dispatcher.utter_template("utter_already_paid_due_date", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow="due_date")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}

        elif value == "cycle_date_issue":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="due_date",delay_reason="cycle_date_issue")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        elif value == "business_loss":
            dispatcher.utter_template("utter_disagree_to_pay_reason_accepted",tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="due_date",delay_reason="business_loss")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        elif value == "insufficient_funds":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="due_date",delay_reason="insufficient_funds")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        
        elif value == "family_dispute":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="due_date",delay_reason="family_dispute")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        
        elif value == "change_account_for_deduction":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="due_date",delay_reason="change_account_for_deduction")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}

        elif value == "account_not_working":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="due_date",delay_reason="account_not_working")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}

        elif value == "foreclosing_through_own_funds":
            dispatcher.utter_template("utter_disagree_to_pay_reason_unaccepted", tracker)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                               disposition_id="delay_reason", flag=TIMEOUT_FLAG,emi_flow="due_date",delay_reason="foreclosing_through_own_funds")
            return {"trail_count": None, "ask_delay_reason": value, "stop_conversation": "TRUE"}
        
        

        return {"ask_delay_reason":None}

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any]
    ) -> List[EventType]:
        return [FollowupAction("action_listen"), AllSlotsReset()] 
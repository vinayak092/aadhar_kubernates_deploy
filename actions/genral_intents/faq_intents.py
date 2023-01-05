
from actions.utils.common_imports import *
from actions.utils.helper import *
import handle_bulk_data

import time

helper = Helper()


class ActionGreet(Action):

    def name(self):
        return 'action_greet'

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message.get("intent").get("name")
        greet_count = tracker.get_slot("greet_count")
        user_message=tracker.latest_message.get("text")
        if intent == "greet":
            requested_slot = tracker.get_slot(REQUESTED_SLOT)
            if greet_count >= 2:
                dispatcher.utter_template("utter_agent_will_connect_common", tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,
                                                   user_message=user_message,flag=TIMEOUT_FLAG,disposition_id="MULTIPLE HELLO")
                return [FollowupAction("action_listen"), AllSlotsReset()]
            return_values = []
            if greet_count > 0:
                print("inside greet_count == 0")
                main_flow = tracker.active_form.get("name")
                print("main_flow",main_flow)
                if main_flow != "user_confirmation_form":
                    return_values.append(SlotSet("main_flow", main_flow))
                current_slot = tracker.get_slot(REQUESTED_SLOT)
                dispatcher.utter_template('utter_ask_capability_pre_due_aadhar', tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="greet")
                return [FollowupAction(tracker.active_form.get("name")), 
                        SlotSet(REQUESTED_SLOT, None),
                        SlotSet("trail_count", get_trail_count(tracker)),
                        SlotSet("greet_count", greet_count + 1)] + return_values
            trail_count = tracker.get_slot("trail_count")
            if tracker.active_form.get("name") is not None and requested_slot == "availability_status" and \
                    trail_count is None:
                print("tracker.active_form.get() is not None")
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="greet")
                dispatcher.utter_template("utter_ask_capability_pre_due_aadhar", tracker)
            else:
                print("tracker.active_form.get() is not None -2")
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="greet")
                dispatcher.utter_template('utter_ask_capability_pre_due_aadhar', tracker)
            print("tracker.active_form.get() is not None -3")
            return get_return_values(tracker) + [SlotSet("greet_count", greet_count + 1)]
        else:
            dispatcher.utter_template('utter_default_common', tracker)
            send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Not understood")
        return get_return_values(tracker)


class ActionWait(Action):

    def name(self):
        return "action_wait"

    def run(self, dispatcher, tracker, domain):
        
        wait_count=tracker.get_slot("wait_count")
        time_diff=0
        if wait_count<2:
            dispatcher.utter_template("utter_customer_informed_wait", tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Wait",flag=WAIT_FLAG)
            return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                FollowupAction(tracker.active_form.get("name")),
                SlotSet("wait_count",wait_count+1)
            ]
        else:
            dispatcher.utter_template('utter_agent_will_connect_common', tracker)
            user_message=tracker.latest_message.get("text")
            # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Human Handoff")
            return [FollowupAction("action_listen"), AllSlotsReset()]


class ActionBye(Action):

    def name(self):
        return "action_bye"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_bye_pre_due_aadhar", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,disposition_id="bye")
        return [FollowupAction("action_listen"), AllSlotsReset()]

class ActionAskBounceCharge(Action):

    def name(self):
        return "ask_bounce_charges_details"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,disposition_id="Loan Info")
        return [FollowupAction("action_listen"), AllSlotsReset()]

class ActionAutodebitIssue(Action):

    def name(self):
        return "action_auto_debit_issue"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,disposition_id="auto debit issue")
        return [FollowupAction("action_listen"), AllSlotsReset()]

class ActionStopdebitIssue(Action):

    def name(self):
        return "action_stop_auto_debit"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,disposition_id="stop auto debit")
        return [FollowupAction("action_listen"), AllSlotsReset()]

class ActionAskInterestRateChange(Action):
    def name(self):
        return "ask_changed_interest_rate"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar", tracker)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,disposition_id="Loan Info")
        return [FollowupAction("action_listen"), AllSlotsReset()]

class ActionAskEmiAmount(Action):

    def name(self):
        return "ask_emi_amount"

    def run(self, dispatcher, tracker, domain):
        emi_count=tracker.get_slot("emi_count")
        total_emi_amount = tracker.get_slot("total_emi_amount")
        due_date = tracker.get_slot("due_date")
        sheet_name = tracker.get_slot("sheet_name")
        emi_flow = tracker.get_slot("emi_flow")
        loan_id = tracker.get_slot("loan_id")
        customer_name = tracker.get_slot("customer_name")
        if emi_count <2:
            dispatcher.utter_template("utter_inform_outstanding_common", tracker,EMI_Amount=total_emi_amount)
            user_message = tracker.latest_message.get("text")
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=DEFAULT_FLAG,disposition_id="Loan Info")
            return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                FollowupAction(tracker.active_form.get("name")),
                SlotSet("emi_count",emi_count+1)
            ]
        else:
            dispatcher.utter_template('utter_agent_will_connect_common', tracker)
            user_message=tracker.latest_message.get("text")
            # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Human Handoff")
            return [FollowupAction("action_listen"), AllSlotsReset()]

# class ActionAskEmiDuedate(Action):

#     def name(self):
#         return "action_ask_due_date"

#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar", tracker)
#         user_message = tracker.latest_message.get("text")
#         send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,flag=TIMEOUT_FLAG,disposition_id="Loan Info")
#         return [FollowupAction("action_listen"), AllSlotsReset()]

class ActionCallLater(Action):
    def name(self):
        return 'action_call_later'

    def run(self, dispatcher, tracker, domain):
        total_emi_amount = tracker.get_slot("total_emi_amount")
        due_date = tracker.get_slot("due_date")
        sheet_name = tracker.get_slot("sheet_name")
        emi_flow = tracker.get_slot("emi_flow")
        loan_id = tracker.get_slot("loan_id")
        customer_name = tracker.get_slot("customer_name")
        if emi_flow == "aadhar_postbounce":
            dispatcher.utter_template("utter_not_avail_talk", tracker,total_emi_amount=total_emi_amount)
        # elif emi_flow == "due_date":
        #     dispatcher.utter_template("utter_not_available_to_talk", tracker,monthly_emi = monthly_emi)
        # elif emi_flow == "dpd_minus_2":
        #     dispatcher.utter_template("utter_not_available_to_talk_DPD_minus_2_DPD_minus_2", tracker,monthly_emi = monthly_emi)
        # elif emi_flow == "dpd_minus_1":
        #     dispatcher.utter_template("utter_not_available_to_talk_DPD_minus_1_DPD_minus_2", tracker,monthly_emi = monthly_emi)
        user_message = tracker.latest_message.get("text")
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, user_message=user_message,
                                           disposition_id="UB", flag=TIMEOUT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionThankYou(Action):

    def name(self):
        return "action_thank_you"

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_user_said_thank_you_common", tracker)
        send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Thank you",emi_flow=emi_flow)
        return get_return_values(tracker)

class ActionVehicleSeized(Action):
    def name(self):
        return 'action_vehicle_seized'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        dispatcher.utter_template('utter_general_queries_customer_care_common', tracker)
        user_message=tracker.latest_message.get("text")
        # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="vehicle seized",user_message=user_message,sheet_name=sheet_name,emi_flow=emi_flow)
        return [FollowupAction("action_listen"), AllSlotsReset()]


# class ActionChangeLanguage(Action):
#     def name(self):
#         return "action_change_language"

#     def run(self, dispatcher, tracker, domain):
#         change_language_count = tracker.get_slot("change_language_count")
#         # Language_order = [hindi,tamil,kannada,telugu,malayalam,bengali,punjabi,marathi,english]
#         supported_languages=[
#                             "हिंदी","कन्नड़","कनाडा","इंग्लिश",
#                             "ಹಿಂದಿ","ಕನ್ನಡ","ಇಂಗ್ಲಿಷ್",
#                             "kannada","hindi","english"]
#         if change_language_count <2:
#             change_specific_language_count=tracker.get_slot("change_specific_language_count")
#             text = tracker.latest_message.get("text")
#             if text:
#                 text = text.lower()
#             print("text:::::::::::::::", text)
#             existed = 0
#             total_emi_amount = tracker.get_slot("total_emi_amount")
#             due_date = tracker.get_slot("due_date")
#             sheet_name = tracker.get_slot("sheet_name")
#             emi_flow = tracker.get_slot("emi_flow")
#             loan_id = tracker.get_slot("loan_id")
#             customer_name = tracker.get_slot("customer_name")
#             link_status= tracker.get_slot("link_status")
#             for lan in supported_languages:
#                 if lan in text:
#                     existed += 1
#             if existed >1 :
#                 dispatcher.utter_custom_json({"language_change": True})
#                 print("Coming here")
#                 send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Language change")
#                 dispatcher.utter_template("utter_language_preference",tracker)
#                 return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE"),SlotSet("change_language_count",change_language_count+1)]
#             elif existed==1:
#                 if "हिंदी" not in text and "ಕನ್ನಡ" not in text and "english" not in text:
#                     if change_specific_language_count<1:
#                         send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Language change")
#                         dispatcher.utter_template("utter_confirm_language_support", tracker)
#                         if user_details['flow_type']=="aadhar_pre_due":
#                             return [FollowupAction(tracker.active_form.get("name")),SlotSet("availability_status",None),SlotSet("payment_confirmation",None),SlotSet("payment_reconfirmation",None),SlotSet("default",None),SlotSet("ask_delay_reason",None),
#                                 SlotSet("trail_count",None),SlotSet("user_confirmation",None), SlotSet(REQUESTED_SLOT, None),SlotSet("change_specific_language_count",change_specific_language_count+1),SlotSet("change_language_count",change_language_count+2)]
#                         else:
#                             return [FollowupAction(tracker.active_form.get("name")),SlotSet("availability_status",None),SlotSet("payment_confirmation",None),SlotSet("payment_reconfirmation",None),SlotSet("default",None),SlotSet("ask_delay_reason",None),
#                                 SlotSet("trail_count",None),SlotSet("user_confirmation",None), SlotSet(REQUESTED_SLOT, None),SlotSet("change_specific_language_count",change_specific_language_count+1),SlotSet("change_language_count",change_language_count+2)]
#                     else:
#                         dispatcher.utter_template("utter_bye_common",tracker)
#                         send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change")
#                         return [FollowupAction("action_listen"),AllSlotsReset()]
#                 print("Coming Thereeeeeee")
#                 dispatcher.utter_template("utter_apology_call_back",tracker)
#                 return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE"),SlotSet("change_language_count",change_language_count+1)]
#             else:
#                 dispatcher.utter_template("utter_apology_call_back", tracker)
#                 send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change")
#                 return [FollowupAction("action_listen"),AllSlotsReset()]
#         else:
#             dispatcher.utter_template("utter_bye_common",tracker)
#             send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change")
#             return [FollowupAction("action_listen"),AllSlotsReset()]
class ActionChangeLanguage(Action):
    def name(self):
        return "action_change_language"

    def run(self, dispatcher, tracker, domain):
        change_language_count = tracker.get_slot("change_language_count")
        user_details = get_user_details(tracker)
        # total_loans=get_total_loan(tracker)
        # total_emi_amount,due_date,sheet_name,emi_flow,loan_id,area,bucket_list,template_id,ptp_days,customer_name,customer_status = get_emi_details(tracker,total_loans)
        # Language_order = [hindi,tamil,kannada,telugu,malayalam,bengali,punjabi,marathi,english]
        # supported_languages=["हिंदी","इंग्लिश","अंग्रेजी","अंग्रेज़ी",
        #                     "ஹிந்தி","தமிழ்","மலையாளம்","மராத்தி","பஞ்சாபி","இங்கிலீஷ்","ஆங்கிலம்","ஆங்கிலத்தில்",
        #                     "ഹിന്ദി","തമിഴ്","മലയാളം","മറാത്തി","ഇംഗ്ലീഷ്",
        #                     "ਤਾਮਿਲ","ਹਿੰਦੀ","ਮਲਿਆਲਮ","ਪੰਜਾਬੀ","ਮਰਾਠੀ","અંગ્રેજી","ਅੰਗਰੇਜ਼ੀ",
        #                     "तामिळ","मल्याळम","મલયાલમ",
        #                     "hindi","હિન્દી","english","अंग्रेज",
        #                     "குஜராத்தி","ഗുജറാത്തി","ਗੁਜਰਾਤੀ","अंग्रेज़ी"]
        supported_languages = ["हिंदी","इंग्लिश","अंग्रेजी","अंग्रेज़ी","hindi","english","अंग्रेज","अंग्रेज़ी"]
        if change_language_count <2:
            change_specific_language_count=tracker.get_slot("change_specific_language_count")
            text = tracker.latest_message.get("text")
            if text:
                text = text.lower()
            print("text:::::::::::::::", text)
            existed = 0
            for lan in supported_languages:
                if lan in text:
                    existed += 1
            if existed >2:
                dispatcher.utter_custom_json({"language_change": True})
                print("Coming here")
                send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="language_change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
                dispatcher.utter_template("utter_language_preference_pre_due_aadhar",tracker)
                return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE"),SlotSet("change_language_count",change_language_count+1)]
            elif existed==1 or existed==2:
                # if "हिंदी" not in text and "ગુજરાતી" not in text:
                if change_specific_language_count<1:
                    dispatcher.utter_template("utter_confirm_language_support_common",tracker)
                    send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="language_change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
                    return [FollowupAction(tracker.active_form.get("name")),SlotSet("availability_status",None),SlotSet("payment_confirmation",None),SlotSet("payment_reconfirmation",None),SlotSet("default",None),SlotSet("ask_delay_reason",None),SlotSet("trail_count",None),SlotSet("user_confirmation",None), SlotSet(REQUESTED_SLOT, None),SlotSet("change_specific_language_count",change_specific_language_count+1),SlotSet("change_language_count",change_language_count+2)]
                    # else:
                    #     dispatcher.utter_template("utter_bye_common",tracker)
                    #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
                    #     return [FollowupAction("action_listen"),AllSlotsReset()]
                print("Coming Thereeeeeee")
                dispatcher.utter_template("utter_apology_call_back_pre_due_aadhar",tracker)
                return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE"),SlotSet("change_language_count",change_language_count+1)]
            else:
                dispatcher.utter_template("utter_apology_call_back_pre_due_aadhar", tracker)
                send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="language_change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
                return [FollowupAction("action_listen"),AllSlotsReset()]
        else:
            dispatcher.utter_template("utter_bye_pre_due_aadhar",tracker)
            send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="language_change")
            return [FollowupAction("action_listen"),AllSlotsReset()]

        # if "english" in text and "hindi" in text:
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE")]
        # if "हिंदी" in text and ("अंग्रेज़ी" in text or "इंग्लिश" in text):
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE")]
        # if "hindi" in text:
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen")]
        # if "english" in text or "हिंदी" in text:
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen"), SlotSet("language_recheck", "TRUE")]
        # if "अंग्रेजी" in text or "इंग्लिश" in text:
        #     'क्या आप अंग्रेजी में बदल सकते हैं'
        #     print("this is working-----------------")
        #     dispatcher.utter_custom_json({"language_change": True})
        #     send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",language=user_details['language'],outstanding_payment=user_details['EMI Amount'],emi_flow=user_details['flow_type'])
        #     return [FollowupAction("action_listen")]
        # other_languages = ["telugu", "tamil"]
        # for item in other_languages:
        #     if item in text.lower():
        # dispatcher.utter_template("utter_apology_call_back", tracker, language=item)
        # # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher, disposition_id="Language change")
        # send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",sheet_name=sheet_name, emi_flow=emi_flow)
        # return [FollowupAction("action_listen")]


# class ActionChangeLanguageFromEnglishToHindi(Action):
#     def name(self):
#         return "action_change_language_from_english_to_hindi"

#     def run(self, dispatcher, tracker, domain):
#         emi_flow=tracker.get_slot("emi_flow")
#         sheet_name=tracker.get_slot("sheet_name")
#         language_recheck = tracker.get_slot("language_recheck")
#         print("Language Recheck:",language_recheck)
#         if language_recheck:
#             main_flow = tracker.active_form.get("name")
#             current_slot = tracker.get_slot(REQUESTED_SLOT)
#             send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="English to Hindi",sheet_name=sheet_name,emi_flow=emi_flow)
#             return [FollowupAction("language_recheck_form"), SlotSet(REQUESTED_SLOT, None),
#                     SlotSet("main_flow", main_flow), SlotSet("current_slot", current_slot)]
#         send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Language change",sheet_name=sheet_name,emi_flow=emi_flow)
#         dispatcher.utter_template("utter_confirm_language_support_common", tracker)
#         return [FollowupAction("action_repeat")]


# class ActionChangeLanguageFromHindiToEnglish(Action):
#     def name(self):
#         return "action_change_language_from_hindi_to_english"

#     def run(self, dispatcher, tracker, domain):
#         sheet_name=tracker.get_slot("sheet_name")
#         emi_flow=tracker.get_slot("emi_flow")
#         language_recheck = tracker.get_slot("language_recheck")
#         print("**** Language Recheck:",language_recheck)
#         if language_recheck:
#             main_flow = tracker.active_form.get("name")
#             current_slot = tracker.get_slot(REQUESTED_SLOT)
#             send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Hindi to English",sheet_name=sheet_name,emi_flow=emi_flow)
#             return [FollowupAction("language_recheck_form"), SlotSet(REQUESTED_SLOT, None),
#                     SlotSet("main_flow", main_flow), SlotSet("current_slot", current_slot)]
#         send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Language change",sheet_name=sheet_name,emi_flow=emi_flow)
#         dispatcher.utter_template("utter_confirm_language_support_common", tracker)
#         return [FollowupAction("action_repeat")]


# class ActionLanguageChange(Action):
#     def name(self):
#         return "action_language_change"

#     def run(self, dispatcher, tracker, domain):
#         emi_flow=tracker.get_slot("emi_flow")
#         sheet_name=tracker.get_slot("sheet_name")
#         text = tracker.latest_message.get("text")
#         print("Language Text:",text)
#         if "hindi" in text:
#             dispatcher.utter_custom_json({"language_change": True})
#             send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",sheet_name=sheet_name,emi_flow=emi_flow)
#             return [FollowupAction("action_listen")]
#             pass
#         if "अंग्रेज़ी" in text or "इंग्लिश" in text:
#             pass
#         dispatcher.utter_message("Yes, i can change speak in")
#         send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Language change",sheet_name=sheet_name,emi_flow=emi_flow)
#         return get_return_values(tracker)


# class ActionNoise(Action):
#     def name(self):
#         return "action_noise"

#     def run(self, dispatcher, tracker, domain):
#         timestamp = tracker.get_slot("timestamp")
#         if timestamp is None:
#             return [FollowupAction("action_listen")]
#         noise_count = tracker.get_slot("noise_count")
#         current_timestamp = time.time()
#         difference = current_timestamp - timestamp
#         print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", difference)
#         updated_time_limit = 60 - difference
#         send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Noise")
#         if int(updated_time_limit) > 0:
#             helper.send_conversation_flag(WAIT_FLAG, dispatcher, time_limit=int(updated_time_limit))
#             if int(noise_count) > 6:
#                 dispatcher.utter_template("utter_report_noise", tracker)
#                 return [FollowupAction("action_listen"), SlotSet("noise_count", 0)]
#             else:
#                 return [FollowupAction("action_listen"), SlotSet("noise_count", int(noise_count) + 1)]
#         else:
#             return [FollowupAction("action_no_message")]


class ActionDefault(Action):

    def name(self):
        return 'action_default'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        default_count=tracker.get_slot("default_count")
        print(default_count,"default_count-1")
        if default_count<2:
            dispatcher.utter_template('utter_default_common', tracker)
            send_and_store_disposition_details(tracker,dispatcher,flag=DEFAULT_FLAG,disposition_id="Not understood",emi_flow=emi_flow)
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("default_count",default_count+1)
            ]
        else:
            dispatcher.utter_template("utter_agent_will_connect_common",tracker)
            send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="Human handoff",emi_flow=emi_flow)
            return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionHumanHandOff(Action):
    def name(self):
        return 'action_human_handoff'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template('utter_human_handoff_common', tracker)
        user_message=tracker.latest_message.get("text")
        # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Human Handoff",user_message=user_message,emi_flow=emi_flow)
        return [FollowupAction("action_listen"), AllSlotsReset()]


class ActionAskCapability(Action):

    def name(self):
        return 'action_ask_capability'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_ask_capability_pre_due_aadhar", tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="bot capability",emi_flow=emi_flow)
        return get_return_values(tracker)


class ActionNoMessage(Action):
    def name(self):
        return "action_no_message"

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        no_response_count = tracker.get_slot("no_response_count")
        latest_event = tracker.events
        previous_message_no_message = True
        user_message_flag = False
        for event in reversed(latest_event):
            if event["event"] == "user":
                if user_message_flag:
                    if event["text"] == "/no_message":
                        previous_message_no_message = False
                        break
                    else:
                        break
                if event["text"] == "/no_message":
                    user_message_flag = True
                    continue
                elif event["text"] == "/noise":
                    no_response_count = None
                    break

        if previous_message_no_message:
            no_response_count = None
        print("No Response count:",no_response_count)
        if no_response_count is None:
            if tracker.active_form.get("name") is not None:
                dispatcher.utter_template("utter_idle_common", tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message="no_message", flag=DEFAULT_FLAG,disposition_id="No Response",emi_flow=emi_flow)
                return [
                    SlotSet(REQUESTED_SLOT, None),
                    SlotSet("trail_count", get_trail_count(tracker)),
                    FollowupAction(tracker.active_form.get("name")),
                    SlotSet("no_response_count", 1)
                ]
            dispatcher.utter_template("utter_idle_common", tracker)
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message="no_message", flag=DEFAULT_FLAG,disposition_id="No Response",emi_flow=emi_flow)
            return [FollowupAction("action_listen"), SlotSet("no_response_count", 1)]
        else:
            if no_response_count >= 2:
                dispatcher.utter_template("utter_idle_bye_common", tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,user_message="no_message", flag=TIMEOUT_FLAG,disposition_id="No Response",emi_flow=emi_flow)
                return [FollowupAction("action_listen"), AllSlotsReset()]
            else:
                if tracker.active_form.get("name") is not None:
                    dispatcher.utter_template("utter_idle_common", tracker)
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="No Response",emi_flow=emi_flow)
                    return [
                        SlotSet(REQUESTED_SLOT, None),
                        SlotSet("trail_count", get_trail_count(tracker)),
                        FollowupAction(tracker.active_form.get("name")),
                        SlotSet("no_response_count", int(no_response_count) + 1)
                    ]
                dispatcher.utter_template("utter_idle_common", tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="No Response",emi_flow=emi_flow)
                return [FollowupAction("action_listen"), SlotSet("no_response_count", int(no_response_count) + 1)]


class ActionHumiliate(Action):

    def name(self):
        return 'action_humiliate'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template('utter_apology_common', tracker)
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="apology",emi_flow=emi_flow)
        return get_return_values(tracker)


class ActionCustomerCareGeneralIntents(Action):
    def name(self):
        return 'action_general_queries_customer_care'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common", tracker)
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="general query",emi_flow=emi_flow)
        return get_return_values(tracker)


class ActionRepeat(Action):
    def name(self):
        return 'action_repeat'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        repeat_count=tracker.get_slot("repeat_count")
        if repeat_count<3:
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="ask repeat",emi_flow=emi_flow)
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            SlotSet("repeat_count", repeat_count+1),
            FollowupAction(tracker.active_form.get("name")),
        ]
        else:
            dispatcher.utter_template('utter_human_handoff_common', tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Human Handoff",emi_flow=emi_flow)
            return [FollowupAction("action_listen"),AllSlotsReset()]

# class ActionLateFees(Action):

#     def name(self):
#         return 'action_late_fees'

#     def run(self, dispatcher, tracker, domain):
#         emi_flow = tracker.get_slot("emi_flow")
#         dispatcher.utter_template("utter_human_handoff_common",tracker)
#         send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask late fees", flag=TIMEOUT_FLAG,emi_flow=emi_flow)
#         return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionAskInterestRate(Action):

    def name(self):
        return 'action_ask_interest_rate'
        
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask interest rate", flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionAsklateFees(Action):

    def name(self):
        return 'action_ask_late_fees'
       
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="late fees", flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionWillPaylateFee(Action):

    def name(self):
        return 'action_will_pay_late_fee'
       
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="late fees", flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionTransferToAnotherHfc(Action):
    def name(self):
        return "action_transfer_to_another_hfc"
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Transfer Account",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPrincipalAmountLeft(Action):

    def name(self):
        return 'action_principal_amount_left'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask principal amount left",flag=TIMEOUT_FLAG)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionLoanCancellation(Action):

    def name(self):
        return 'action_loan_cancellelation'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_out_of_scope_pre_due_aadhar",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="loan cancellation",flag=TIMEOUT_FLAG)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionTenureLeft(Action):

    def name(self):
        return 'action_tenure_left'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask tenure left",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class MoratoriumPeriod(Action):

    def name(self):
        return 'action_moratorium_period'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask moratorium period",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ChangeEmiDate(Action):

    def name(self):
        return 'action_change_emi_due_date'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="change emi due date",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionCycleDateIssue(Action):
    def name(self):
        return "action_cycle_date_issue"
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Inform_wrong_info",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ReduceEmi(Action):
    def name(self):
        return 'action_reduce_emi'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask reduce emi",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionAskNextDueDate(Action):
    def name(self):
        return 'action_next_due_date'

    def run(self, dispatcher, tracker, domain):
        due_date_count =tracker.get_slot("due_date_count")
        emi_flow = tracker.get_slot("emi_flow")
        if due_date_count <2:
            dispatcher.utter_template("utter_human_handoff_common",tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask next due date",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
            return [FollowupAction("action_listen"), AllSlotsReset()]
        else:
            dispatcher.utter_template('utter_agent_will_connect_common', tracker)
            user_message=tracker.latest_message.get("text")
            # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Human Handoff")
            return [FollowupAction("action_listen"), AllSlotsReset()]



class ActionAskBalanceOrPaymentTillNow(Action):
    def name(self):
        return 'action_balance_payment'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask balance payment",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionInformPaymentDone(Action):
    def name(self):
        return 'action_inform_payment_done'

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_bye_pre_due_aadhar",tracker)
        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, disposition_id="Paid", flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"), AllSlotsReset()]

class ActionAskDueDate(Action):
    def name(self):
        return 'ask_emi_due_date'

    def run(self, dispatcher, tracker, domain):
        due_date = tracker.get_slot("due_date")
        sheet_name = tracker.get_slot("sheet_name")
        emi_flow = tracker.get_slot("emi_flow")
        due_date=datetime.datetime.strptime(due_date,"%d-%m-%Y").date()
        due_date=due_date.strftime("%d %B %Y")
        dispatcher.utter_template("utter_inform_past_payment_date_common",tracker,EMI_Date=due_date)
        # dispatcher.utter_template("utter_repeat_ask_payment_pre_due",tracker)
        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="ask due date",flag=DEFAULT_FLAG,sheet_name=sheet_name,emi_flow=emi_flow)
        return get_return_values(tracker)

class ActionInformHaveBalance(Action):
    def name(self):
        return "action_inform_have_balance"
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        link_status =tracker.get_slot("link_status")
        if link_status == "YES":
            dispatcher.utter_template("utter_agree_to_pay_pre_due_aadhar",tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="inform_have_balance",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        else:
            dispatcher.utter_template("utter_agree_pay_2_pre_due_aadhar",tracker)
            dispatcher.utter_template("utter_no_call_back_time_pre_due_aadhar",tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="inform_have_balance",flag=TIMEOUT_FLAG,emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionInsufficientFunds(Action):
    def name(self):
        return "action_insufficient_funds"
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_financial_reason_pre_due_aadhar",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,delay_reason="Insufficient Funds",emi_flow=emi_flow,disposition_id="delay_reason")
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionMedicalIssue(Action):
    def name(self):
        return "action_medical_issue"
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        link_status =tracker.get_slot("link_status")
        if emi_flow == "aadhar_pre_due":
            if link_status == "YES":
                dispatcher.utter_template("utter_non_financial_reason_pre_due_aadhar",tracker)
            else:
                dispatcher.utter_template("utter_non_financial_reason_2_pre_due_aadhar",tracker)
        entities = tracker.latest_message["entities"]
        given_date = ""
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    try:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,delay_reason="medical issue",emi_flow=emi_flow,disposition_id="delay_reason")
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionFamilyIssue(Action):
    def name(self):
        return "action_family_dispute_issue"
    def run(self, dispatcher, tracker, domain): 
        emi_flow = tracker.get_slot("emi_flow")
        entities = tracker.latest_message["entities"]
        given_date = ""
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    try:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        dispatcher.utter_template("utter_non_financial_reason_pre_due_aadhar",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,delay_reason="family dispute",emi_flow=emi_flow,disposition_id="delay_reason")
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionSalaryIssue(Action):
    def name(self):
        return "salary_issue"
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        link_status =tracker.get_slot("link_status")
        if emi_flow == "aadhar_pre_due":
            if link_status == "YES":
                dispatcher.utter_template("utter_financial_reason_pre_due_aadhar",tracker)
            else:
                dispatcher.utter_template("utter_financial_reason_2_pre_due_aadhar",tracker)
        entities = tracker.latest_message["entities"]
        given_date = ""
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    try:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,delay_reason="salary issue",emi_flow=emi_flow,ptp_date=given_date,disposition_id="delay_reason")
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionTechnicalIssue(Action):
    def name(self):
        return "action_technical_issue"
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        link_status =tracker.get_slot("link_status")
        if emi_flow == "aadhar_pre_due":
            if link_status == "YES":
                dispatcher.utter_template("utter_non_financial_reason_pre_due_aadhar",tracker)
            else:
                dispatcher.utter_template("utter_non_financial_reason_2_pre_due_aadhar",tracker)
        entities = tracker.latest_message["entities"]
        given_date = ""
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    try:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,delay_reason="technical issue",emi_flow=emi_flow,disposition_id="delay_reason",ptp_date=given_date)
        return [FollowupAction("action_listen"),AllSlotsReset()]



class ActionJobLosslIssue(Action):
    def name(self):
        return "action_job_loss"
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        link_status =tracker.get_slot("link_status")
        if emi_flow == "aadhar_pre_due":
            if link_status == "YES":
                dispatcher.utter_template("utter_financial_reason_pre_due_aadhar",tracker)
            else:
                dispatcher.utter_template("utter_financial_reason_2_pre_due_aadhar",tracker)
        entities = tracker.latest_message["entities"]
        given_date = ""
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,delay_reason="job loss",emi_flow=emi_flow,disposition_id="delay_reason",ptp_date=given_date)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionBusinessIssue(Action):
    def name(self):
        return "action_business_loss_issue"
    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        link_status =tracker.get_slot("link_status")
        print("In ActionBusinessIssue",emi_flow)
        print("In ActionBusinessIssue",link_status)
        if emi_flow == "aadhar_pre_due":
            if link_status == "YES":
                print("enter here business>>>>>",link_status)
                dispatcher.utter_template("utter_financial_reason_pre_due_aadhar",tracker)
            else:
                dispatcher.utter_template("utter_financial_reason_2_pre_due_aadhar",tracker)
        entities = tracker.latest_message["entities"]
        given_date = ""
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    try:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,delay_reason="business issue",emi_flow=emi_flow,disposition_id="delay_reason",ptp_date=given_date)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionInformWrongInfo(Action):
    def name(self):
        return "action_inform_wrong_info"
    def run(self, dispatcher, tracker, domain):
        due_date = tracker.get_slot("due_date")
        due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y")
        due_date = due_date.strftime("%d %B %Y")
        dispatcher.utter_template("utter_customer_dispute_in_loan_pre_due_aadhar",tracker,cycle_date=due_date)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="Inform_wrong_info")
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionThirdParty(Action):
    def name(self):
        return "action_third_party_contact"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_agent_will_connect_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="NRPC")
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionForeclosingThroughOwnFunds(Action):
    def name(self):
        return "action_foreclosing_through_own_funds"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="foreclosing through own funds")
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionChangeAccountForDeduction(Action):
    def name(self):
        return "action_change_account_for_deduction"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="change account for deduction")
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionAccountNotWorking(Action):
    def name(self):
        return "action_account_not_working"
    def run(self, dispatcher, tracker, domain):
        link_status =tracker.get_slot("link_status")
        emi_flow = tracker.get_slot("emi_flow")
        given_date = ""
        if emi_flow == "aadhar_pre_due":
            if link_status == "YES":
                dispatcher.utter_template("utter_non_financial_reason_pre_due_aadhar",tracker)
            else:
                dispatcher.utter_template("utter_non_financial_reason_2_pre_due_aadhar",tracker)
        entities = tracker.latest_message["entities"]
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    try:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="account not working")
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPayViaAgent(Action):
    def name(self):
        return "action_pay_via_agent"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="pay via agent")
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionAskPaymentMethod(Action):
    def name(self):
        return "action_ask_payment_method"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="ask payment method")
        return [FollowupAction("action_listen"),AllSlotsReset()]




# class ActionAskNextDueDate(Action):
#     def name(self):
#         return "action_ask_next_due_date"
#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar",tracker)
#         send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="Loan Onfo")
#         return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionAskProductDetails(Action):
    def name(self):
        return "action_ask_product_details"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_know_more_about_loan_pre_due_aadhar",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="ask product details")
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionBranchIssue(Action):
    def name(self):
        return "action_branch_issue"
    def run(self,dispatcher, tracker, domain):
        link_status =tracker.get_slot("link_status")
        emi_flow = tracker.get_slot("emi_flow")
        given_date = ""
        if emi_flow == "aadhar_pre_due":
            if link_status == "YES":
                dispatcher.utter_template("utter_non_financial_reason_pre_due_aadhar",tracker)
            else:
                dispatcher.utter_template("utter_non_financial_reason_2_pre_due_aadhar",tracker)
        entities = tracker.latest_message["entities"]
        given_date = ""
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    try:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,delay_reason="branch issue",disposition_id="delay_reason")
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPayViaBranch(Action):
    def name(self):
        return "action_pay_via_branch"
    def run(self,dispatcher, tracker, domain):
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="pay via branch")
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionPayViaStore(Action):
    def name(self):
        return "action_pay_via_store"
    def run(self,dispatcher, tracker, domain):
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="pay via store")
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionPayViaOnline(Action):
    def name(self):
        return "action_pay_via_online"
    def run(self,dispatcher, tracker, domain):
        dispatcher.utter_template("utter_human_handoff_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="pay via online")
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionOutOfContext(Action):

    def name(self):
        return "action_out_of_context"

    def run(self, dispatcher, tracker, domain):
        total_loans=get_total_loan(tracker)
        emi_flow = tracker.get_slot("emi_flow")
        # total_emi_amount,due_date,sheet_name,emi_flow,loan_id,area,bucket_list,template_id,ptp_days,customer_name,customer_status = get_emi_details(tracker,total_loans)
        dispatcher.utter_template("utter_out_of_scope_pre_due_aadhar", tracker)
        send_and_store_disposition_details(tracker,dispatcher,flag=TIMEOUT_FLAG,disposition_id="out of scope",emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionDeathInFamily(Action):
    def name(self):
        return "action_death_in_family"
        
    def run(self, dispatcher, tracker, domain):
        total_loans=get_total_loan(tracker)
        given_date = ""
        emi_flow = tracker.get_slot("emi_flow")
        if emi_flow == "aadhar_pre_due":
            dispatcher.utter_template("utter_death_pre_due_aadhar",tracker)
        entities = tracker.latest_message["entities"]
        given_date = ""
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    try:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,delay_reason="death in family",ptp_date=given_date,emi_flow=emi_flow,disposition_id="Death")
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionPersonalIssue(Action):
    def name(self):
        return "action_personal_issue"

    def run(self,dispatcher, tracker, domain):
        link_status =tracker.get_slot("link_status")
        emi_flow = tracker.get_slot("emi_flow")
        if emi_flow == "aadhar_pre_due":
            if link_status == "YES":
                dispatcher.utter_template("utter_non_financial_reason_pre_due_aadhar",tracker)
            else:
                dispatcher.utter_template("utter_non_financial_reason_2_pre_due_aadhar",tracker)
        entities = tracker.latest_message["entities"]
        given_date = ""
        if entities:
            for entity in entities:
                if entity.get("entity") == "date":
                    try:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except:
                        given_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    given_date = given_date.strftime("%d %B %Y")
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,emi_flow=emi_flow,disposition_id="delay_reason",delay_reason="personal issue")
        return [FollowupAction("action_listen"),AllSlotsReset()]

class ActionAskPaymentLink(Action):
    def name(self):
        return "action_ask_payment_link"

    def run(self, dispatcher, tracker, domain):
        emi_flow = tracker.get_slot("emi_flow")
        dispatcher.utter_template("utter_general_queries_customer_care_common",tracker)
        send_and_store_disposition_details(tracker=tracker,flag=TIMEOUT_FLAG, dispatcher=dispatcher,disposition_id="ask payment link",emi_flow=emi_flow)
        return [FollowupAction("action_listen"),AllSlotsReset()]


class ActionInitialMessage(Action):
    def name(self):
        return "action_initial_message"
    def run(self,dispatcher,tracker,domain):
        sender_id = tracker.sender_id
        data = handle_bulk_data.detect_camapin(sender_id)
        print("data--------------->",data)
        if data == "yes":
            total_loans=get_total_loan(tracker)
            total_emi_amount,due_date,sheet_name,emi_flow,loan_id,customer_name,link_status,language=get_emi_details(tracker,total_loans)
            due_date = due_date[0]
        else:
            user_details=get_user_details_redis(tracker)
            emi_flow=user_details.get("emi_flow")
            total_emi_amount = user_details.get("total_emi_amount")
            due_date = user_details.get("due_date")
            sheet_name = user_details.get("sheet_name")
            customer_name = user_details.get("customer_name")
            # if (customer_name)=="Arvind":
            #     customer_name = customer_name
            # else:
            #     customer_name="Arvind"
            loan_id =user_details.get("loan_id")
            link_status=user_details.get("link_status").upper()
            language=user_details.get("language")
        sheet_name = ""
        print("emi_flow-------------->",emi_flow)
        if emi_flow =="aadhar_pre_due":
            return [FollowupAction("aadhar_pre_due_form"),SlotSet("emi_flow",str(emi_flow)),SlotSet("total_emi_amount",str(total_emi_amount)),SlotSet("loan_id",str(loan_id)),SlotSet("due_date",str(due_date)),SlotSet("customer_name",str(customer_name)),SlotSet("sheet_name",str(sheet_name)),SlotSet("link_status",str(link_status)),SlotSet("language",str(language))]
        # if emi_flow == "due_date":
        #     return [FollowupAction("post_emi_form"),SlotSet("emi_flow",emi_flow),SlotSet("total_emi_amount",total_emi_amount),SlotSet("loan_id",loan_id),SlotSet("due_date",due_date),SlotSet("customer_name",customer_name),SlotSet("sheet_name",sheet_name)]
        # if emi_flow == "dpd_minus_2":
        #     return [FollowupAction("dpd2_form"),SlotSet("emi_flow",emi_flow),SlotSet("total_emi_amount",total_emi_amount),SlotSet("loan_id",loan_id),SlotSet("due_date",due_date),SlotSet("customer_name",customer_name),SlotSet("sheet_name",sheet_name)]
        # if emi_flow =="dpd_minus_1":
        #     return [FollowupAction('dpd1_form'),SlotSet("emi_flow",emi_flow),SlotSet("total_emi_amount",total_emi_amount),SlotSet("loan_id",loan_id),SlotSet("due_date",due_date),SlotSet("customer_name",customer_name),SlotSet("sheet_name",sheet_name)]
        # if emi_flow =="aadhar_postbounce":
        #     return [FollowupAction('aadhar_postbounce_form'),SlotSet("emi_flow",emi_flow),SlotSet("total_emi_amount",total_emi_amount),SlotSet("loan_id",loan_id),SlotSet("due_date",due_date),SlotSet("customer_name",customer_name),SlotSet("sheet_name",sheet_name)]
        # else:
        #     return [FollowupAction("dpd2_form"),SlotSet("emi_flow",emi_flow),SlotSet("total_emi_amount",total_emi_amount),SlotSet("loan_id",loan_id),SlotSet("due_date",due_date),SlotSet("customer_name",customer_name),SlotSet("sheet_name",sheet_name)]
        
#!/bin/bash

exec  python get_customer_details.py &
exec  python -m rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core.yml --port 8650 -vv &
exec  python -m rasa run actions --actions actions.actions --port 5650 -vv &
exec  python nlu/emi_english/app.py &
exec  python nlg/emi_english/nlg_server.py &
exec  python Orchestrator/CZ/orchestrator.py --port 7114 &

exec  python -m rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core_hindi.yml --port 8550 -vv &
exec  python -m rasa run actions --actions actions.actions --port 5550 -vv &
exec  python nlu/emi_english/app_hindi.py &
exec  python nlg/emi_english/nlg_server_hindi.py &
exec  python Orchestrator/CZ/orchestrator_hindi.py --port 8001 

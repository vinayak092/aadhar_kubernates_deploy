
exec python nlu/emi_english/app.py &
exec python nlg/emi_english/sampleNLG.py &
exec python  -m rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core.yml --port 8025 -vv &
exec python -m rasa run actions --actions actions.actions --port 5025 -vv &
exec python Orchestrator/CZ/orchestrator.py



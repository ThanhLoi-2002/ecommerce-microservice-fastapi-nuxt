# 1) Create & activate virtualenv
python -m venv venv
# Windows
.\venv\Scripts\activate

pip install -r requirements.txt

pip freeze > requirements.txt

run uvicorn app.main:app --reload

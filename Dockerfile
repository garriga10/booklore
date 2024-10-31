FROM python:3.10-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY package_folder package_folder
COPY package_folder/models package_folder/models
COPY raw_data raw_data

CMD uvicorn package_folder.api_file:app --host 0.0.0.0 --port $PORT

FROM python:3.10-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY package_folder/workflow package_folder/workflow
COPY package_folder/workflow/models/model-reco-2.pkl package_folder/workflow/models/model-reco-2.pkl
COPY raw_data raw_data

CMD uvicorn package_folder.workflow.api_file:app --host 0.0.0.0 --port $PORT

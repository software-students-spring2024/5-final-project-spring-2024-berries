FROM python:3.10

WORKDIR /backend_api

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP google_api.py

EXPOSE 5002

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5002"]

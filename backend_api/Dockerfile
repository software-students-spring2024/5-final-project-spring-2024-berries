FROM python:3.10

WORKDIR /machine_learning_client

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5002"]

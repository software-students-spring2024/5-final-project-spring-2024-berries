FROM python:3.10

WORKDIR /web_app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP app.py

EXPOSE 5001

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]

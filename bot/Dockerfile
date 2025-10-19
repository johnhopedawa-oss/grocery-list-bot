FROM python:3.12-slim 

WORKDIR /bot

COPY . .

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 80

CMD ["python", "telegrambot.py"]
FROM python:3.11-slim
WORKDIR /app
COPY . .
EXPOSE 80
RUN pip3 install -r requirements.txt
CMD uvicorn main:app --reload --host 0.0.0.0 --port 8080

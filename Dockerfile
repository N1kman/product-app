FROM python:3.12

COPY . .

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["alembic", "upgrade", "head"]

CMD ["uvicorn", "src.main:main_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# with certs
#CMD ["uvicorn", "src.main:main_app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--ssl-keyfile", "../certs/key.pem", "--ssl-certfile", "../certs/cert.pem"]


FROM python:3.12

COPY . .

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "src.main:main_app", "--host", "0.0.0.0", "--port", "8000"]


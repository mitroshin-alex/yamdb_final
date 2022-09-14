FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY ./ ./

CMD ["python3", "manage.py", "migrate"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api_yamdb.wsgi"]

RUN python manage.py collectstatic --no-input
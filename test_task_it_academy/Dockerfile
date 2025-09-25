FROM python:3.11.9

RUN apt-get update && apt-get install -y postgresql-client

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "test_task_it_academy.wsgi:application", "--bind", "0.0.0.0:8000"]
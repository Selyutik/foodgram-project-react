FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN apt update && \
    apt upgrade -y && \
    apt -y install gcc && \
    python3 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir && \
    pip3 install gunicorn

COPY . ./

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
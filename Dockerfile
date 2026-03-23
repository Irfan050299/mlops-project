FROM python:3.12.3

WORKDIR /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["bash", "entrypoint.sh"]
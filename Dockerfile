FROM python:3.9.6

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "main.main:app", "--host", "0.0.0.0", "--port", "80"]

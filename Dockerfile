FROM python:3.11
WORKDIR /usr/src/app
ENV PYTHONPATH=vladimirPay
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "backend/manage.py", "runserver", "0.0.0.0:8000"]
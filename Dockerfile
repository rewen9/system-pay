FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
ENV PYTHONPATH=vladimirPay
COPY requirements.txt .

# Создание и активация виртуальной среды
RUN apt install python3
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "backend/manage.py", "runserver", "0.0.0.0:8000"]
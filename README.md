# system-pay
Система контроля транзакций.

# Start:
Работает с Postgres (14-16 версии).

- Установить зависимости из requiriments,

Сделать миграцию:
- env PYTHONPATH=~/vladimirPay python3 backend/manage.py migrate

Запустить:
- env PYTHONPATH=~/vladimirPay python3 backend/manage.py runserver 0.0.0.0:8000

Для удобного теста потребуется postman. В него загрузить system-payments.postman_collection.json

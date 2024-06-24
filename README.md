# Agendamento de serviços

## First install
- Environment variables

- ## Celery ([docs] (https://docs.celeryq.dev/en/stable/))
- O Celery precisa de um worker ()Run `celery -A config worker -B` to start the celery worker
  - Alternative alias command: `make celery`
- Run `celery -A config flower` to start flower in http://127.0.0.1:5555/
  - Alternative alias command: `make flower`

# Agendamento de serviços

## Início
- Clonar o repositório:
  
`https://github.com/epfolletto/service_scheduling.git`

- Na raiz do projeto, utilizando [Poetry](https://python-poetry.org/):
  
`Poetry install`

## Banco de dados

- Encontra as mudanças nos esquemas do banco de dados:

`make mmg (poetry run python3 manage.py makemigrations)`
  
- Aplica as migrações:
`make migreate (poetry run python3 manage.py migrate)`


<!--
## Celery ([docs] (https://docs.celeryq.dev/en/stable/))
- O Celery precisa de um worker ()Run `celery -A config worker -B` to start the celery worker
  - Alternative alias command: `make celery`
- Run `celery -A config flower` to start flower in http://127.0.0.1:5555/
  - Alternative alias command: `make flower`
 
- ## Celery ([docs] (https://docs.celeryq.dev/en/stable/))

- ## Celery ([docs] (https://docs.celeryq.dev/en/stable/))
--> 

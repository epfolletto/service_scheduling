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
  
`make migrate (poetry run python3 manage.py migrate)`

## [Celery](https://docs.celeryq.dev/en/stable/)

- O Celery precisa de um worker (RabbitMQ, Redis, Amazon SQS). Como recomendação, pode-se utilizar o [Redis](https://redis.io/) com docker:

`make redis (docker run -d -p 6379:6379 redis)`

- O comando para ligar o Celery pode ser:

`(make cl) celery -A tasks worker -l info --pool=solo`

- Para monitorar as tarefas de forma gráfica, pode-se utilizzar o [Flower](https://flower.readthedocs.io/en/latest/):

`(make fl) celery -A tasks flower --address=127.0.0.1 --port=5566`

## [Celery](https://docs.celeryq.dev/en/stable/)
- Para iniciar o projeto:
  
`make run (poetry run python3 manage.py runserver)`
 

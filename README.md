API Development with FastAPI, SQLAlchemy, Alembic, PostgreSQL, Uvicorn and Docker. In this tutorial we take a first look at building an API with FastAPI building an API using FastAPI with Uvicorn (Get and Post Data),
SQLAlchemy + Alembic to manage migrations, PostgreSQL + PGAdmin  all wrapped deployed in Docker/Docker-Compose.

---
### Docker services commands
Build the docker image for the fastapi backend application:\
`docker-compose build --no-cache`

Start only the api:\
`docker-compose --project-name fastapi-ltier2 up api`

Start all the application services:\
`docker-compose --project-name fastapi-ltier2 up`

---
### Alembic migrations
Command for alembic initialization:\
`alembic init ./src/migrations`

To do the 'make migration', changes or revisions:\
`docker compose exec api /bin/bash -c "alembic revision --autogenerate -m 'my message'"` \
**_or_**\
`docker exec -it fastapi-ltier2 /bin/bash -c "alembic revision --autogenerate -m 'my message'"`

To migrate the new changes/revisions:\
`docker-compose exec api /bin/bash -c "alembic upgrade head"`\
`docker exec -it fastapi-ltier2 /bin/bash -c "alembic upgrade head"`

---
### Other useful docker commands
Clean all containers and dangling images:\
`docker kill $(docker ps -q); docker container rm $(docker ps -a -q) && docker image rm $(docker images --filter "dangling=true" -q)`

---
### Open the api in the browser
http://localhost:8000/docs

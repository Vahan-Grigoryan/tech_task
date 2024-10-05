FROM python:3.11

RUN mkdir -p project_root
WORKDIR project_root

COPY . .

RUN apt-get update && \
    pip install -r requirements.txt

# I use "alembic downgrade" for tests always work over clear tables in db 
# without rebuild(--build option for docker-compose) images
ENTRYPOINT alembic downgrade base && \
    alembic upgrade head && \
    python -m pytest

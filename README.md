## This project is tech task for job(temporary)

I create this project in 2 days, before that days I do other tech tasks, thanks for understanding.
Project uses FastAPI and besides default functionality described in tech task, it have these opportunities for:

- JWT Auth
- To rate cats
- Docker support
- Tests(partially, only for auth, deadline time...)



### Before using project

Run following:
```
pip install -r requirements.txt
alembic downgrade base
alembic upgrade head
```

### Run project

With docker:
```
docker compose up --build
```

Without docker:
```
python main.py
```

### Run tests

With docker
```
docker compose -f docker-compose-tests.yml up --build
```

Without docker:
```
python -m pytest
```

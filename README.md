# AWS-resource-chatbot

The purpose of this project is to enable monitoring resources in AWS. It's just a fun personal project with external apis and AWS.


## Local

This project runs as a Flask API with Redis. You can use Docker or a local venv.

### Option A: Docker

```bash
docker-compose up --build
```

If you need to stop containers or inspect logs:

```bash
docker-compose down
docker-compose logs -f api
```

Environment variables are loaded from `.env`. Start by copying `.env.example` and filling in values:

```bash
cp .env.example .env
```

Required keys:
- `PORT`
- `DATABASE_PATH`
- `TEST_ACCOUNT_SID`
- `TEST_AUTH_TOKEN`

Required when `TESTING=False`:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`

Required when `DEBUG=False`:
- `FROM_PHONE_NUMBER`
- `PFROM_PHONE_NUMBER_SID`

The API listens on `http://localhost:3000`.

### Option B: Virtualenv

```bash
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install -r api/requirements/prod.txt
python api/wsgi.py
```

The API listens on `http://localhost:3000`.


### Database Setup

The project uses a local SQLite database under `api/data/`.

```bash
# from repo root
mkdir -p api/data
sqlite3 api/data/user.db < api/data/schema.sql
```

After adding the database, generate `api/app/models.py` via

```
sqlacodegen sqlite:///api/data/user.db
```

## Testing

Before running any unittests, I highly recommend adding a virtual environment and adding test requirements

```bash
# from ~/path/to/aws-sms-monitor/
python3 -m venv virtualenv
source virtualenv/bin activate
pip install -r requirements/test.txt
```

If you ever leave the project, running 

```bash
deactivate 
```

In order to run the tests, 

```bash
# from ~/path/api/aws-sms-monitor/
python -m unittest discover api/testing/ 
```

All tests must pass before merging.

## Contributing

Any help in testing, development, documentation and other tasks is highly appreciated and useful to the project. However, still in the design stage, so I'm a little less inclined for outside help until it's all sorted out. 

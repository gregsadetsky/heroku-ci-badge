# how to dev

## requirements

- Python 3

## install steps

- create virtual environment
- activate it, `source venv/bin/activate`
- install requirements, `pip -r requirements.txt`

## developing

- set local environment variables: `HEROKU_AUTH_TOKEN`, `PIPELINE_ID`, `REDIS_URL` and `CACHE_TIMEOUT`
-- `export HEROKU_AUTH_TOKEN="...."`, etc.
- run `gunicorn app:app`

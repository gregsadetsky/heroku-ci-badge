import os
import logging

import redis
from heroku import get_last_test_run_status
from flask import Flask, send_from_directory, redirect
from nocache import nocache

app = Flask(__name__)

# https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f
if __name__ != '__main__':
  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)

BADGE_DIR = './badges'
CACHE_TIMEOUT_DEFAULT = 900
REDIS_CONNECT_TIMEOUT = 10
BADGES_ENUM = ('succeeded', 'failed', 'errored')
FILES_ENUM = BADGES_ENUM + ('error',)

def send_badge_file(badge):
  assert badge in FILES_ENUM
  return send_from_directory(
    BADGE_DIR,
    '{}.svg'.format(badge)
  )

@app.route('/')
def index():
  return redirect('/last.svg')


@app.route('/last.svg')
@nocache
def last_test():
  # check presence of mandatory env vars
  if os.getenv('HEROKU_AUTH_TOKEN') is None:
    app.logger.info('mandatory HEROKU_AUTH_TOKEN env var not set (see README.md)')
    return send_badge_file('error')

  if os.getenv('PIPELINE_ID') is None:
    app.logger.info('mandatory PIPELINE_ID env var not set (see README.md)')
    return send_badge_file('error')

  if os.getenv('REDIS_URL') is None:
    app.logger.info('mandatory REDIS_URL env var not set (did you provision a redis add-on?)')
    return send_badge_file('error')

  r = redis.from_url(os.environ.get('REDIS_URL'), socket_connect_timeout=REDIS_CONNECT_TIMEOUT)

  try:
    # is there a cached result?
    result = r.get('build_result')
  except redis.exceptions.ConnectionError:
    app.logger.error('could not connect to redis')
    return send_badge_file('error')

  if result is not None:
    # good to go -- return cached result
    return send_badge_file(result.decode('ascii'))

  # no cached result, fetch info from heroku
  result = get_last_test_run_status()
  if result is None:
    # network error, wrong credentials, etc.
    app.logger.error('could not get result from Heroku')
    return send_badge_file('error')

  if result not in BADGES_ENUM:
    # fallback in case of unexpected result
    app.logger.error('got unexpected build status: {}'.format(result))
    return send_badge_file('error')
    
  # at this point, we have a good result

  cache_timeout = os.getenv('CACHE_TIMEOUT', str(CACHE_TIMEOUT_DEFAULT))
  # the given timeout is valid
  # or there was no given timeout (will then use default)
  if cache_timeout.isdigit():
    cache_timeout = int(cache_timeout)
  else:
    # we were given a timeout, but in an incorrect format
    app.logger.error('CACHE_TIMEOUT is not a valid int')
    cache_timeout = CACHE_TIMEOUT_DEFAULT

  # since we have a good result, cache it
  res = r.set('build_result', result, ex=cache_timeout)

  return send_badge_file(result)

import os

from flask import Flask, send_from_directory
from heroku import get_last_test_run_status
import redis

app = Flask(__name__)

BADGE_DIR = 'badges'
CACHE_TIMEOUT_DEFAULT = 900
RESULT_TO_BADGE = {
  'succeeded': 'pass',
  'failed': 'fail'
}

def send_badge_file(badge):
  print('send_from_directory', badge)
  return send_from_directory(
    BADGE_DIR,
    '{}.svg'.format(badge)
  )

@app.route('/last.svg')
def last_test():
  # check presence of mandatory env vars
  if os.getenv('HEROKU_AUTH_TOKEN') is None or \
      os.getenv('PIPELINE_ID') is None or \
      os.getenv('REDIS_URL') is None:
    app.logger.info('1 or more mandatory env vars not set (see README)')
    return send_badge_file('error')

  # TODO catch error (wrong redis credentials) and log it
  r = redis.from_url(os.environ.get('REDIS_URL'))

  # is there a cached result?
  result = r.get('build_result')
  if result is not None:
    return send_badge_file(result.decode('ascii'))

  # no cached result, fetch info from heroku
  result = get_last_test_run_status()
  if result is None:
    # network error, wrong credentials, etc.
    app.logger.error('could not get result from Heroku')
    return send_badge_file('error')

  if result not in RESULT_TO_BADGE:
    # fallback in case of unexpected result
    app.logger.error('got unexpected build status: {}'.format(result))
    return send_badge_file('error')
    
  # at this point, we have a good result

  cache_timeout = os.getenv('CACHE_TIMEOUT', str(CACHE_TIMEOUT_DEFAULT))
  # the given timeout is valid
  # or there was no given timeout (will then use default)
  if cache_timeout.isdigit():
    cache_timeout = int(CACHE_TIMEOUT_DEFAULT)
  else:
    # we were given a timeout, but in an incorrect format
    app.logger.error('CACHE_TIMEOUT is not a valid int')
    cache_timeout = CACHE_TIMEOUT_DEFAULT

  badge = RESULT_TO_BADGE[result]

  # since we have a good result, cache it
  r.set('build_result', badge, ex=cache_timeout)

  return send_badge_file(badge)

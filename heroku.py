import os
import requests

import flask


HEROKU_API_SERVER = 'https://api.heroku.com/'

def do_request(path):
  r = requests.get(
    '{}{}'.format(HEROKU_API_SERVER, path),
    headers={
      'Accept': 'application/vnd.heroku+json; version=3',
    }
  )

  if not r.status_code == requests.codes.ok:
    flask.current_app.logger.error('heroku returned status code {}'.format(r.status_code))
    return None

  return r.json()

def get_last_test_run_status():
  pipeline_id = os.getenv('PIPELINE_ID')
  assert pipeline_id is not None, 'PIPELINE_ID not set'

  res = do_request(
    'pipelines/{}/test-runs'.format(pipeline_id),
  )

  # wrong pipeline id, heroku error, etc.
  if res is None:
    return None

  if len(res) == 0:
    flask.current_app.logger.error('pipeline has no test results')
    return None

  # unexpected result
  if 'status' not in res[0]:
    flask.current_app.logger.error('no `status` found for latest test result')
    return None

  return res[0]['status']

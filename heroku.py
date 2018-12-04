import os
import requests

import flask


HEROKU_API_SERVER = 'https://api.heroku.com/'

def do_request(path):
  api_token = os.getenv('HEROKU_AUTH_TOKEN')
  assert api_token is not None, 'HEROKU_AUTH_TOKEN not set'

  s = requests.session()
  # disable using local netrc.
  # simplifies local development as the netrc heroku CLI
  # credentials should not be used here.
  # https://github.com/requests/requests/issues/2773
  s.trust_env = False
  result = s.get(
    '{}{}'.format(HEROKU_API_SERVER, path),
    headers={
      'Accept': 'application/vnd.heroku+json; version=3',
      'Authorization': 'Bearer {}'.format(api_token)
    }
  )

  if not result.status_code == requests.codes.ok:
    flask.current_app.logger.error('heroku returned status code {}'.format(result.status_code))
    return None

  return result.json()

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

  found_status = None
  for result in res:
    if 'status' not in result:
      continue
    # skip currently building/running tests to return first 'final' result
    if result['status'] in ['building', 'running']:
      continue
    found_status = result['status']
    break
  else:
    flask.current_app.logger.error('could not find any build status')
    return None

  return found_status

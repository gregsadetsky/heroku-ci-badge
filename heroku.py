import os

import requests


HEROKU_API_SERVER = 'https://api.heroku.com/'

def do_request(path, extra_headers=None):
  api_token = os.getenv('HEROKU_AUTH_TOKEN')
  assert api_token is not None, 'HEROKU_AUTH_TOKEN not set'

  headers = {
    'Accept': 'application/vnd.heroku+json; version=3',
    'Authorization': 'Bearer {}'.format(api_token)
  }
  if extra_headers:
    headers.update(extra_headers)

  # TODO handle case where credential is incorrect
  # TODO handle other generic errors
  # TODO log to console in all cases
  # TODO return None

  r = requests.get(
    '{}{}'.format(HEROKU_API_SERVER, path),
    headers=headers
  )

  return r.json()

def get_last_test_run_status():
  pipeline_id = os.getenv('PIPELINE_ID')
  assert pipeline_id is not None, 'PIPELINE_ID not set'

  extra_headers = {
    'Range': 'id ..; max=1;'
  }

  # TODO handle case where pipeline id is incorrect, log to console
  res = do_request(
    'pipelines/{}/test-runs'.format(pipeline_id),
    extra_headers=extra_headers
  )

  # network error
  if res is None:
    return None

  if len(res) == 0:
    return None

  return res[0]['status']

if __name__ == '__main__':
  get_last_test_run()

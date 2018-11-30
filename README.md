# heroku-ci-badge

Get a Heroku CI badge for your repo's README file.

![example badge](badges/pass.svg)


## Requirements

- Have a Heroku app
- Have a [Heroku Pipeline](https://devcenter.heroku.com/articles/pipelines) configured for that app
- Use [Heroku CI](https://devcenter.heroku.com/articles/heroku-ci) for that pipeline


## Steps

### Deploy this app to your account

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Note the deployed app name -- you'll need it for later.

TODO check -- does procfile auto-start web worker?
TODO check -- does heroku app setup asp for env variable values?

### Create an authorization token

    HEROKU_AUTH_TOKEN=`heroku authorizations:create -s "read" -S -d "heroku ci badge"`

### Set the token as an environment variable on the app

    heroku config:set HEROKU_AUTH_TOKEN=`echo $HEROKU_AUTH_TOKEN` -a {deployed app name}

### Set the ID of your pipeline as an environment variable on the app

    heroku config:set PIPELINE_ID="{pipeline ID}" -a {deployed app name}

Note that this should be the UUID of the pipeline (`9478101b-...`) rather than the name (`myapp-pipeline`) of the pipeline.

### Test the badge

    heroku apps:open /last.svg -a {deployed app name}

### Insert the badge into your README.md

    [![Heroku CI Status](https://{deployed app name}.herokuapp.com/last.svg)](https://dashboard.heroku.com/pipelines/{pipeline ID}/tests)

### Optional

Change how frequently the build result badge refreshes by setting the `CACHE_TIMEOUT` env var (in seconds). The default value is 15 minutes.

    heroku config:set CACHE_TIMEOUT="300" -a {deployed app name}

Note that a shorter cache period will result in more calls to the Heroku API, which may lead to elevated errors.

Setting a `CACHE_TIMEOUT` to `0` is _strongly_ discouraged.


## Notes

If you're seeing...

![error badge](badges/error.svg)

... instead of a pass/fail mark, it means that the heroku-ci-badge app cannot retrieve the build status.
- Check that you've set the `HEROKU_AUTH_TOKEN` environment variable on your app
- Check that your auth token is valid by running `heroku authorizations`. Is your token in that list?
- Check that you've set the `PIPELINE_ID` environment variable on your app
- Check that the `PIPELINE_ID` value is valid by checking the pipeline URL https://dashboard.heroku.com/pipelines/{pipeline ID}
- Check the app's log outputs for errors

    heroku log -a {deployed app name}


## TODO

- Test incorrect heroku credentials
- Test incorrect pipeline id
- Test heroku error response

- Heroku deploy button (app.json?)
- Dog food: test & have badge for this app!
- Check that -s scope read is enough to get build status (need read-protected? more?)

- Support more than 1 pipeline (use /pipelines/{ID}/x.svg path?)
- Support master and other branches (use /{branch}.svg and /piplines/{branch}.svg ?)


## Thanks

- [Shields.io](https://shields.io/) for the dynamic shield svg
- Ismar Slomic for the [question & motivation](https://stackoverflow.com/questions/50918181/heroku-ci-status-badge)
- Heroku, for being awesome.


## Disclaimers

- This software is provided as is.
- This project has no affiliation with Heroku.

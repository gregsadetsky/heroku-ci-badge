# heroku-ci-badge

Get a Heroku CI badge for your repo's README file.

TODO insert badge


## Steps

### Deploy this app to your account

TODO insert deploy to heroku button

Note the app name -- you'll need it later

### Create an authorization token

    HEROKU_AUTH_TOKEN=`heroku authorizations:create -s "read" -S -d "heroku ci badge"`

### Set the token as an environment variable on the app

    heroku config:set HEROKU_AUTH_TOKEN=`echo $HEROKU_AUTH_TOKEN` -a {deployed app name}

### Set the ID of your pipeline as an environment variable on the app

    heroku config:set PIPELINE_ID="{pipeline ID}" -a {deployed app name}

### Test the badge

    heroku apps:open /last.svg -a {deployed app name}

### Insert the badge into your README.md

    [![Heroku CI Status](https://{deployed app name}.herokuapp.com/last.svg)](https://dashboard.heroku.com/pipelines/{pipeline ID}/tests)


## Notes

If you're seeing...

![error badge](badges/error.svg)

... instead of a pass/fail mark, it means that the heroku-ci-badge app cannot retrieve the build status.
- Check that you've set the `HEROKU_AUTH_TOKEN` environment variable on your app
- Check that your auth token is valid by running `heroku authorizations`. Is your token in that list?
- Check that you've set the `PIPELINE_ID` environment variable on your app
- Check that the `PIPELINE_ID` value is valid by checking the pipeline URL https://dashboard.heroku.com/pipelines/{pipeline ID}


## TODO

- Heroku deploy button (app.json?)
- Dog food: badge for this app!
- Check that -s scope read is enough to get build status (need read-protected? more?)

- Support more than 1 pipeline (use /pipelines/{ID}/x.svg path?)
- Support master and other branches (use /{branch}.svg and /piplines/{branch}.svg ?)

## Thanks

- [Shields.io](https://shields.io/) for the dynamic shield svg
- Ismar Slomic for the [question & motivation](https://stackoverflow.com/questions/50918181/heroku-ci-status-badge)
- Heroku, for being awesome.

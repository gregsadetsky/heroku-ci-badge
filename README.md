# heroku-ci-badge

Get a Heroku CI badge for your repo's README file.

![example badge](badges/succeeded.svg)


## Requirements

- A Heroku app
- A [Heroku Pipeline](https://devcenter.heroku.com/articles/pipelines) configured for that app
- Use [Heroku CI](https://devcenter.heroku.com/articles/heroku-ci) for that pipeline


## Steps

### Deploy this app to your account (this sets up a free dyno and a free Redis addon)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

During the setup, you will be asked to fill out two environment variables:

#### HEROKU_AUTH_TOKEN

Generate a token using

    heroku authorizations:create -s "read" -S -d "heroku-ci-badge"

#### PIPELINE_ID

This should be the UUID of the pipeline to which Heroku CI is attached (`9478101b-...`) rather than the name of the pipeline (`myapp-pipeline`).

### Once the app has been deployed, click the "View" button to see it.

You will be redirected to `/last.svg`, the URL for the dynamic badge.

### Insert the badge into your README.md

    [![Heroku CI Status](https://{deployed app name}.herokuapp.com/last.svg)](https://dashboard.heroku.com/pipelines/{pipeline ID}/tests)

### Optional

Change how frequently the build result badge refreshes by setting the `CACHE_TIMEOUT` environment var (in seconds). The default value is 15 minutes.

    heroku config:set CACHE_TIMEOUT="300" -a {deployed app name}

Note that a shorter cache period will result in more calls to the Heroku API, which may lead to elevated errors.

Setting `CACHE_TIMEOUT` to `0` is _strongly_ discouraged.


## Notes

If you're seeing...

![error badge](badges/error.svg)

... instead of a pass/fail mark, it means that the heroku-ci-badge app could not retrieve the build status.
- Check that you've set the `HEROKU_AUTH_TOKEN` environment variable on your app
- Check that your auth token is valid by running `heroku authorizations` . Note that token IDs (shown in the list) and the token values are not the same. Do you see the `heroku-ci-badge` token generated previously? If you run `heroku authorizations:info {token id}` is the `Token: ` value the same as the one you set as the `HEROKU_AUTH_TOKEN` environment variable?
- Check that you've set the `PIPELINE_ID` environment variable on your app
- Check that the `PIPELINE_ID` value is valid by checking the pipeline URL https://dashboard.heroku.com/pipelines/{pipeline ID}
- Check the app's log outputs for errors: `heroku log -a {deployed app name}`


## Updating the app

Updating the app's code once it's deployed is not as easy as doing the initial deployment (i.e., it's not a single click). Based on the instructions [here](https://f-a.nz/dev/update-deploy-to-heroku-app/), here are the steps to update deployed `heroku-ci-badge` apps:

    cd {some directory}
    git init
    heroku git:remote -a {deployed app name}
    git remote add origin https://github.com/gregsadetsky/heroku-ci-badge
    git pull origin master
    git push heroku master


## TODO

- Support more than 1 pipeline (use /pipelines/{ID}/x.svg ?)
- Support master and other branches (use /{branch}.svg and /pipelines/{branch}.svg ?)
- Dogfood: use Heroku CI & show badge for this app


## Thanks

- [Shields.io](https://shields.io/) for the shield svg.
- Ismar Slomic for the [question & motivation](https://stackoverflow.com/questions/50918181/heroku-ci-status-badge).
- Heroku, for being awesome.


## Disclaimers

- This software is provided as is.
- This project has no affiliation with Heroku.

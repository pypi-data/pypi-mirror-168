import json

import beam


def valid_reconstruction(app: beam.App):
    dumped_app = app.dumps()
    dumped_json = json.dumps(dumped_app)
    app_from_dumped_config = beam.App.from_config(json.loads(dumped_json))
    return app_from_dumped_config.dumps() == dumped_app


def test_basic_app_reconstruction():
    app = beam.App(
        name="some_app",
        cpu="4000m",
        memory="128mi",
        gpu=5,
    )

    assert valid_reconstruction(app)


def test_adding_triggers_correctly_should_succeed():
    app = beam.App(
        name="some_app",
        cpu="4000m",
        memory="128mi",
        gpu=5,
    )

    app.Trigger.CronJob(
        inputs={
            "some_input": beam.Types.String,
        },
        cron_schedule="asda",
    )
    app.Trigger.Webhook(inputs={"name": beam.Types.String})
    app.Trigger.RestAPI(
        inputs={"name": beam.Types.String}, outputs={"name": beam.Types.String}
    )

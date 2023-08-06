import json
import beam
import pytest

from beam.types import PythonVersion
from beam.utils import compose_cpu, compose_memory


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
        python_packages=["vim"],
        python_version=PythonVersion.Python36,
        workspace="./some_folder",
    )

    assert valid_reconstruction(app)


def test_adding_triggers_correctly_should_succeed():
    app = beam.App(
        name="some_app",
        cpu=1,
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


def test_compose_cpu():
    assert compose_cpu(1) == "1000m"
    assert compose_cpu(0.25) == "250m"
    assert compose_cpu(1.999) == "1999m"
    assert compose_cpu("1000m") == "1000m"


def test_compose_memory():
    assert compose_memory("10gi") == "10Gi"
    assert compose_memory("10 gi ") == "10Gi"
    assert compose_memory("10 Gi ") == "10Gi"

    # Raises if Gi is > 256
    with pytest.raises(ValueError):
        compose_memory("10000Gi")

    assert compose_memory("256mi") == "256Mi"
    assert compose_memory("256 mi ") == "256Mi"
    assert compose_memory("256 Mi ") == "256Mi"

    # Raises if Mi is < 128 or >= 1000
    with pytest.raises(ValueError):
        compose_memory("127Mi")

    with pytest.raises(ValueError):
        compose_memory("1000Mi")

    # Test invalid formats
    with pytest.raises(ValueError):
        compose_memory("1000ti")

    with pytest.raises(ValueError):
        compose_memory("1000.0")

    with pytest.raises(ValueError):
        compose_memory("1000")

    with pytest.raises(ValueError):
        compose_memory("2 gigabytes")


def test_cpu_in_app_config():
    config = {"name": "some_app", "memory": "128mi"}

    app1 = beam.App(
        **config,
        cpu=4,
    )

    app2 = beam.App(
        **config,
        cpu="4000m",
    )

    assert valid_reconstruction(app1)
    assert valid_reconstruction(app2)
    assert app1.dumps() == app2.dumps()

    app3 = beam.App(
        **config,
        cpu=0.25,
    )

    app4 = beam.App(**config, cpu="250m")

    assert valid_reconstruction(app3)
    assert valid_reconstruction(app4)
    assert app3.dumps() == app4.dumps()

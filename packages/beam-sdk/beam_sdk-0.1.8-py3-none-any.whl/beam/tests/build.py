# TEMPORARY TEST CASE
import json
from beam.scripts.build import build
from beam.app import App

def test_build_and_rebuild():
    
    # print(build())
    config_json = build()

    config = json.loads(config_json)

    rebuild: App = App.from_config(config)

    assert json.dumps(rebuild.dumps(), indent=4) == config_json

test_build_and_rebuild()
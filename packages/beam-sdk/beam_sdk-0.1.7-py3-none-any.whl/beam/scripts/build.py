import importlib
import inspect
import io
import json
import sys

from beam import App


def build() -> str:
    app_modules = importlib.import_module(("app"))
    beamapp = None

    for member in inspect.getmembers(app_modules):
        member_value = member[1]
        if isinstance(member_value, App):
            beamapp = member_value
            break

    if beamapp is not None:
        return json.dumps(beamapp.dumps())
    
    raise Exception("Beam app not found")

if __name__ == "__main__":
    save_stdout = sys.stdout
    sys.stdout = None
    app_config = build()
    sys.stdout = save_stdout
    print(app_config)

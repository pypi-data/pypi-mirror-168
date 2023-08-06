import beam

app = beam.App(
    name="some_app",
    cpu="4000m",
    memory="128mi",
    gpu=5,
    python_version="python3.8",
    apt_install=[],
    python_packages=["torch", "numpy"],
)


app.Trigger.Webhook(inputs={"name": beam.Types.String})
app.Outputs.File(name="model", path="./outputs/model.ptk")
app.Outputs.Dir(name="model", path="./outputs/modelasasd.ptk")

import json

dumped_json = json.dumps(app.dumps(), indent=4)
print(app.dumps() == beam.App.from_config(json.loads(dumped_json)).dumps())

print(beam.App.from_config(json.loads(dumped_json)).dumps())

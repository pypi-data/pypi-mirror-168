from typing import List
from beam.trigger import TriggerManager
from beam.types import PythonRuntime
from beam.serializer import AppConfigurationSerializer
from beam.dataclass import AppConfiguration


class App:
    def __init__(
        self,
        *,
        name: str,
        cpu: int,
        memory: str,
        python_runtime: PythonRuntime = PythonRuntime.Python38,
        gpu: int = 0,
        apt_install: List[str] = [],
        python_packages: List[str] = [],
        workspace: str = "./"
    ) -> None:
        self.app_config: AppConfiguration = {
            "name": name,
            "cpu": cpu,
            "gpu": gpu,
            "memory": memory,
            "apt_install": apt_install,
            "python_runtime": python_runtime,
            "python_packages": python_packages,
            "workspace": workspace
        }

        AppConfigurationSerializer().validate(self.app_config, raise_exception=True)

        self.Trigger: TriggerManager = TriggerManager()

    def dumps(self):
        return {"app": self.app_config, "triggers": self.Trigger.dumps()}

    @staticmethod
    def from_config(config: dict) -> "App":
        app_config = config.get("app")
        triggers = config.get("triggers")

        app = App(**app_config)
        app.Trigger.from_config(triggers)

        return app

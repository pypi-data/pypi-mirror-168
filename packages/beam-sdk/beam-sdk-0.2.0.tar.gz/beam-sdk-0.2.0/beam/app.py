from typing import List

from beam.base import AbstractDataLoader
from beam.configs.outputs import OutputManager
from beam.configs.trigger import TriggerManager
from beam.dataclass import AppConfiguration
from beam.serializer import AppConfigurationSerializer
from beam.types import PythonRuntime


class App(AbstractDataLoader):
    def __init__(
        self,
        *,
        name: str,
        cpu: int,
        memory: str,
        gpu: int = 0,
        python_runtime: PythonRuntime = PythonRuntime.Python38,
        apt_install: List[str] = [],
        python_packages: List[str] = [],
        workspace: str = "./"
    ) -> None:
        self.app_config = AppConfiguration(
            name=name,
            cpu=cpu,
            gpu=gpu,
            memory=memory,
            apt_install=apt_install,
            python_runtime=python_runtime,
            python_packages=python_packages,
            workspace=workspace,
        )

        AppConfigurationSerializer().validate(
            self.app_config.to_dict(), raise_exception=True
        )

        self.Trigger = TriggerManager()
        self.Outputs = OutputManager()

    def dumps(self):
        return {
            "app": self.app_config.to_dict(),
            "triggers": self.Trigger.dumps(),
            "outputs": self.Outputs.dumps(),
        }

    @staticmethod
    def from_config(config: dict) -> "App":
        app_config = config.get("app")
        triggers = config.get("triggers")
        outputs = config.get("outputs")

        app = App(**app_config)
        app.Trigger.from_config(triggers)
        app.Outputs.from_config(outputs)

        return app

from typing import List, Union
from beam.base import AbstractDataLoader
from beam.configs.outputs import OutputManager
from beam.configs.trigger import TriggerManager
from beam.dataclass import AppConfiguration
from beam.serializer import AppConfigurationSerializer
from beam.types import PythonVersion
from beam.utils import compose_cpu, compose_memory


class App(AbstractDataLoader):
    def __init__(
        self,
        *,
        name: str,
        cpu: Union[str, int],
        memory: str,
        gpu: int = 0,
        apt_install: List[str] = [],
        python_version: PythonVersion = PythonVersion.Python38,
        python_packages: List[str] = [],
        workspace: str = "./"
    ) -> None:
        """
        Keyword Arguments:
            name: the unique identifier for your app
            cpu: total total cpu cores allocated to app
            memory: total amount of memory you to allocate to your app
                - in format [Number][Mi|Gi]
                - e.g. 12Gi or 250Mi
            (Optional) gpu: total gpu cores to allocate to app
            (Optional) apt_install: system level dependencies you want installed into the app
                - e.g. libssl-dev
            (Optional) python_version: version of python available under PythonVersion class
            (Optional) python_packages: python packages you want to install for every runtime
                - e.g. "torch" or "torch==1.12.0"
            (Optional) workspace: directory to continously sync to app during development
        """
        self.app_config = AppConfiguration(
            name=name,
            cpu=compose_cpu(cpu),
            gpu=gpu,
            memory=compose_memory(memory),
            apt_install=apt_install,
            python_version=python_version,
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

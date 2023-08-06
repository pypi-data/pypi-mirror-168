from dataclasses import dataclass
from typing import Dict, List

from beam.base import BaseDataClass
from beam.types import OutputType, PythonRuntime, Types


@dataclass()
class AppConfiguration(BaseDataClass):
    name: str
    cpu: int
    gpu: int
    memory: str
    apt_install: PythonRuntime
    python_runtime: List[str]
    python_packages: List[str]
    workspace: str

@dataclass
class WebhookConfiguration(BaseDataClass):
    inputs: Dict[str, Types]


@dataclass
class CronJobConfiguration(BaseDataClass):
    inputs: Dict[str, Types]
    cron_schedule: str

@dataclass
class RestAPIConfiguration(BaseDataClass):
    inputs: Dict[str, Types]
    outputs: Dict[str, Types]

@dataclass
class FileConfiguration(BaseDataClass):
    path: str
    name: str
    output_type: OutputType

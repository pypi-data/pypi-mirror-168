from dataclasses import dataclass
from typing import Dict, List
from beam.types import PythonRuntime, Types

@dataclass
class AppConfiguration:
    name: str
    cpu: int
    gpu: int
    memory: str
    apt_install: PythonRuntime
    python_runtime: List[str]
    python_packages: List[str]
    workspace: str

@dataclass
class WebhookConfiguration:
    input: Dict[str, Types]


@dataclass
class CronJobConfiguration:
    input: Dict[str, Types]
    cron_schedule: str

@dataclass
class RestAPIConfiguration:
    input: Dict[str, Types]
    output: Dict[str, Types]
from typing import List

from beam.base import AbstractDataLoader, BaseConfiguration
from beam.dataclass import FileConfiguration
from beam.types import OutputType


class File(BaseConfiguration):
    def __init__(self, path: str, name: str, output_type: str):
        self.config =FileConfiguration(
            path=path,
            name=name,
            output_type=output_type
        )


class OutputManager(AbstractDataLoader):
    def __init__(self) -> None:
        self.files: List[File] = []
        self.dirs: List[File] = []

    def File(self, path: str, name: str, **_):
        self.files.append(File(
            path=path,
            name=name,
            output_type=OutputType.File
        ))

    def Dir(self, path: str, name: str, **_):
        self.dirs.append(File(
            path=path,
            name=name,
            output_type=OutputType.Directory
        ))

    def dumps(self):
        return [
            *[f.dumps() for f in self.files],
            *[d.dumps() for d in self.dirs],
        ]

    def from_config(self, outputs: List[dict]):
        if outputs is None:
            return

        for f in outputs:
            if f.get("output_type") == OutputType.Directory:
                self.Dir(**f)
            else:
                self.File(**f)

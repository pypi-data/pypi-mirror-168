# tools for working with data stores

from dataclasses import dataclass
from typing import Dict, Set
from pathlib import Path
from logging import info

@dataclass
class Store:

    @property
    def names_files(self) -> Set[str]:
        pass

    def put(self, content: bytes, name: str) -> None:
        pass

    def fetch(self, name: str) -> bytes:
        pass

    def clear(self) -> None:
        pass


@dataclass
class Local(Store):
    folder: Path

    @property
    def names_files(self) -> Set[str]:
        return set([path.name for path in self.folder.iterdir()])

    def put(self, content: bytes, name: str) -> None:
        info(f"put in store {self} under name {name}")
        with open(self.folder / name, "wb") as f:
            f.write(content)

    def fetch(self, name: str) -> bytes:
        info(f"fetch from store {self} under name {name}")
        with open(self.folder / name, "rb") as f:
            content = f.read()
        return content

@dataclass
class Memory(Store):

    def __post_init__(self):
        self.files: Dict[str, bytes] = {}

    @property
    def names_files(self) -> Set[str]:
        return set(self.files.keys())

    def put(self, content: bytes, name: str) -> None:
        info(f"put in store {self} under name {name}")
        self.files[name] =  content

    def fetch(self, name: str) -> bytes:
        info(f"fetch from store {self} under name {name}")
        return self.files[name]

    def clear(self) -> None:
        del self.files
        self.files = {}

memory = Memory()

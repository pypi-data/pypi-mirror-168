from typing import Callable
from joblib import Memory
from dataclasses import dataclass
from pydantic import BaseSettings


class SettingsGCS(BaseSettings):
    bucket_name: str
    project_name: str

    class Config:
        env_prefix = "gcs_"

    @property
    def memory(self) -> Memory:
        return Memory(
            f"{self.bucket_name}/cache",
            backend="gcs",
            verbose=100,
            backend_options={"project": self.project_name},
        )


# @dataclass
# class Cache:
#     memory: Memory
# 
#     def register(self, func: Callable) -> None:
#         self.__setattr__(func.__name__, self.memory.cache(func))

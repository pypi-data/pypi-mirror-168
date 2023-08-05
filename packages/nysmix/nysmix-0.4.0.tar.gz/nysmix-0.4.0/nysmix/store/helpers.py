"""
helper functions for defining stores
"""

from .base import Store, memory, Local
from .google import GoogleCloudStorage
from enum import Enum, auto
from typing import Optional
from pathlib import Path
from nysmix.config.base import VarEnv
from logging import info


class TypeStore(Enum):
    MEMORY = auto()
    LOCAL = auto()
    GOOGLE = auto()


def get_store(type_store: TypeStore, folder: Optional[Path] = None) -> Optional[Store]:
    store: Optional[Store] = None
    if type_store == TypeStore.MEMORY:
        store = memory
    elif type_store == TypeStore.LOCAL:
        assert folder is not None
        store = Local(folder=folder)
    elif type_store == TypeStore.GOOGLE:
        assert folder is not None
        store = GoogleCloudStorage(folder=folder)
    else:
        info("store not found")
    info(f"getting store {store}")
    return store


def get_store_from_env(folder: Optional[Path] = None) -> Optional[Store]:
    return get_store(
        type_store=TypeStore[VarEnv.TYPE_STORE.value],
        folder=folder,
    )

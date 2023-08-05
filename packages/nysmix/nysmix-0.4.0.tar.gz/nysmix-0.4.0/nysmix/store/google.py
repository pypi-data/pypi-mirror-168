# tools for working with google cloud storage as a data store

from dataclasses import dataclass
from functools import cached_property
from .base import Store
from typing import List, Set
from logging import info
from google.oauth2.service_account import Credentials
from google.cloud.storage import Client, Bucket, Blob
from pathlib import Path
from nysmix.config.google import VarEnv


@dataclass
class GoogleCloudStorage(Store):

    folder: Path

    @cached_property
    def cred(self) -> Credentials:
        return Credentials.from_service_account_file(VarEnv.PATH_TO_CRED.value)

    @cached_property
    def client(self) -> Client:
        return Client(credentials=self.cred)

    @cached_property
    def bucket(self) -> Bucket:
        return self.client.get_bucket(VarEnv.NAME_BUCKET.value)

    @property
    def blobs(self) -> List[Blob]:
        return list(self.client.list_blobs(self.bucket, prefix=self.folder))

    @property
    def names_files(self) -> Set[str]:
        return set([Path(blob.name).name for blob in self.blobs])

    def blob(self, name: str) -> Blob:
        return self.bucket.blob(str(self.folder / name))

    def put(self, content: bytes, name: str) -> None:
        info(f"put in store {self} under name {name}")
        self.blob(name).upload_from_string(data=content)

    def fetch(self, name: str) -> bytes:
        info(f"fetch from store {self} under name {name}")
        return self.blob(name).download_as_bytes()

    def clear(self) -> None:
        info(f"clearing the bucket {self}")
        for blob in self.blobs:
            info(f"deleting blob {blob.name}")
            blob.delete()

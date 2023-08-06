import os
from abc import ABCMeta, abstractmethod
from .fileio import FileIO
from typing import List, Any


def _get_basename(content: List[Any]) -> Any:
    return content[0].split("/")[-1]


class BaseStorageBackend(metaclass=ABCMeta):
    """Abstract class of storage backends.

    All backends need to implement two apis: ``get()`` and ``get_text()``.
    ``get()`` reads the file as a byte stream and ``get_text()`` reads the file
    as texts.
    """

    @abstractmethod
    def get(self, filepath):
        pass

    @abstractmethod
    def get_text(self, filepath):
        pass

    @abstractmethod
    def listdir(self, filepath):
        pass


class AliyunOSSBackend(BaseStorageBackend):
    """Aliyun OSS storage backend.

    Args:
        access_key_secret (str): access key of aliyun oss
        endpoint (str): endpoint key of aliyun oss
        access_key_id (str): your access key of aliyun oss
        bucket_name (str): your bucket name of aliyun oss
    """

    def __init__(self, bucket_name, access_key_id, access_key_secret, endpoint, **kwargs):
        try:
            import oss2
        except ImportError:
            raise ImportError("Please install oss2 to enable AliyunOSSBackend.")

        auth = oss2.Auth(access_key_id, access_key_secret)
        self.client = oss2.Bucket(auth, endpoint, bucket_name)

    def get(self, filepath):
        value_buf = self.client.get_object(filepath)
        return value_buf.read()

    def get_text(self, filepath):
        raise NotImplementedError

    def listdir(self, filepath):
        try:
            import oss2
        except ImportError:
            raise ImportError("Please install oss2 to enable AliyunOSSBackend.")
        if FileIO.is_oss_path(filepath):
            filepath = FileIO.get_oss_rel_path(filepath)
        return [obj.key for obj in oss2.ObjectIteratorV2(self.client, prefix=filepath)]


class CephBackend(BaseStorageBackend):
    """Ceph storage backend.

    Args:
        path_mapping (dict|None): path mapping dict from local path to Petrel
            path. When ``path_mapping={'src': 'dst'}``, ``src`` in ``filepath``
            will be replaced by ``dst``. Default: None.
    """

    def __init__(self, path_mapping=None):
        try:
            import ceph
        except ImportError:
            raise ImportError('Please install ceph to enable CephBackend.')

        self._client = ceph.S3Client()
        assert isinstance(path_mapping, dict) or path_mapping is None
        self.path_mapping = path_mapping

    def get(self, filepath):
        filepath = str(filepath)
        if self.path_mapping is not None:
            for k, v in self.path_mapping.items():
                filepath = filepath.replace(k, v)
        value = self._client.Get(filepath)
        value_buf = memoryview(value)
        return value_buf

    def get_text(self, filepath):
        raise NotImplementedError

    def listdir(self, filepath):
        raise NotImplementedError


class PetrelBackend(BaseStorageBackend):
    """Petrel storage backend (for internal use).

    Args:
        path_mapping (dict|None): path mapping dict from local path to Petrel
            path. When `path_mapping={'src': 'dst'}`, `src` in `filepath` will
            be replaced by `dst`. Default: None.
        enable_mc (bool): whether to enable memcached support. Default: True.
    """

    def __init__(self, path_mapping=None, enable_mc=True):
        try:
            from petrel_client import client
        except ImportError:
            raise ImportError('Please install petrel_client to enable '
                              'PetrelBackend.')

        self._client = client.Client(enable_mc=enable_mc)
        assert isinstance(path_mapping, dict) or path_mapping is None
        self.path_mapping = path_mapping

    def get(self, filepath):
        filepath = str(filepath)
        if self.path_mapping is not None:
            for k, v in self.path_mapping.items():
                filepath = filepath.replace(k, v)
        value = self._client.Get(filepath)
        value_buf = memoryview(value)
        return value_buf

    def get_text(self, filepath):
        raise NotImplementedError

    def listdir(self, filepath):
        return self._client.list(filepath)


class HardDiskBackend(BaseStorageBackend):
    """Raw hard disks storage backend."""

    def get(self, filepath):
        filepath = str(filepath)
        with open(filepath, 'rb') as f:
            value_buf = f.read()
        return value_buf

    def get_text(self, filepath):
        filepath = str(filepath)
        with open(filepath, 'r') as f:
            value_buf = f.read()
        return value_buf

    def listdir(self, filepath):
        return os.listdir(filepath)

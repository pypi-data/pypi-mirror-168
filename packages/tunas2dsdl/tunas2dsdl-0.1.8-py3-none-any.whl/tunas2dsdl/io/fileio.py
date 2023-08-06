import re


class FileIO:
    @staticmethod
    def clean(varStr):
        return re.sub('\W|^(?=\d)', '', varStr)

    @classmethod
    def get_oss_rel_path(cls, path: str) -> str:
        bucket_name = cls.get_bucket_name(path)
        return path.replace(f"oss://{bucket_name}/", "")

    @classmethod
    def is_oss_path(cls, path: str) -> bool:
        return path.startswith("oss://")

    @classmethod
    def get_bucket_name(cls, path: str) -> str:
        return path.replace("oss://", "").split("/")[0]

    @classmethod
    def is_ceph_path(cls, path: str) -> bool:
        """Whether the path is from ceph

        Arguments:
            path: A path.

         Returns:
             Whether the path is from ceph.
        """
        return path.startswith("s3://") or ":s3://" in path



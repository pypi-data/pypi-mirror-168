"""
Utility classes and functions for working with AWS.
"""
from enum import auto

from heaobject import root
from typing import Optional


class S3StorageClass(root.EnumAutoName):
    """
    The S3 storage classes. The list of storage classes is documented at
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2, and
    each storage class is explained in detail at
    https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html.
    """
    STANDARD = auto()  # S3 Standard
    REDUCED_REDUNDANCY = auto()  # Reduced Redundancy (RRS)
    GLACIER = auto()  # S3 Glacier Flexible Retrieval
    STANDARD_IA = auto()  # S3 Standard-IR (infrequent access)
    ONEZONE_IA = auto()  # S3 One Zone-IR
    INTELLIGENT_TIERING = auto()  # S3 Intelligent-Tiering
    DEEP_ARCHIVE = auto()  # S3 Glacier Deep Archive
    OUTPOSTS = auto()  # S3 Outposts
    GLACIER_IR = auto()  # S3 Glacier Instant Retrieval
    OTHER = auto()


class S3URIMixin:
    """
    Mixing for adding a S3 URI to a desktop object.
    """

    @property
    def s3_uri(self) -> Optional[str]:
        """
        The object's S3 URI.
        """
        try:
            return self.__s3_uri
        except AttributeError:
            return None

    @s3_uri.setter
    def s3_uri(self, s3_uri: Optional[str]):
        s3_uri_ = str(s3_uri) if s3_uri is not None else None
        if s3_uri_ is not None and not s3_uri_.startswith('s3://'):
            raise ValueError(f'Invalid s3 URI {s3_uri_}')
        self.__s3_uri = s3_uri_

    @property
    def presigned_url(self) -> Optional[str]:
        """
        The object's presigned url.
        """
        try:
            return self.__presigned_url
        except AttributeError:
            return None

    @presigned_url.setter
    def presigned_url(self, presigned_url: Optional[str]):
        presigned_url_ = str(presigned_url) if presigned_url is not None else None
        if presigned_url_ is not None and not presigned_url_.startswith('https://'):
            raise ValueError(f'Invalid presigned URL {presigned_url_}')
        self.__presigned_url = presigned_url_

    def set_s3_uri_from_bucket_and_key(self, bucket: Optional[str], key: Optional[str] = None):
        """
        Creates a S3 URI from the given bucket and key, and sets the s3_uri property with it.

        :param bucket: a bucket name. If None, the object's S3 URI will be set to None.
        :param key: a key (optional).
        """
        if bucket is None:
            self.__s3_uri = None
        else:
            self.__s3_uri = _s3_uri(bucket, key)


def _s3_uri(bucket: str, key: Optional[str]) -> str:
    """
    Creates and returns a S3 URI from the given bucket and key.

    :param bucket: a bucket name (required).
    :param key: a key (optional).
    """
    if bucket is None:
        raise ValueError('bucket is required')
    return f"s3://{bucket}/{key if key is not None else ''}"


class S3StorageClassMixin:
    """
    Mixin for adding a storage class property to a desktop object.
    """

    def __init__(self):
        self.__storage_class = S3StorageClass.STANDARD

    @property
    def storage_class(self) -> S3StorageClass:
        """The AWS S3 storage class of this file."""
        try:
            return self.__storage_class
        except AttributeError:
            return S3StorageClass.STANDARD

    @storage_class.setter
    def storage_class(self, storage_class: S3StorageClass):
        if storage_class is None:
            self.__storage_class = S3StorageClass.STANDARD
        elif isinstance(storage_class, S3StorageClass):
            self.__storage_class = storage_class
        else:
            self.__storage_class = S3StorageClass[storage_class]

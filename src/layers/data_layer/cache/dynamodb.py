import json
import time
import boto3
import logging
from botocore.exceptions import ClientError

from cache.abstract import Cache


class DynamoDBCacheClient(Cache):
    """
    Cache client for DynamoDB table.

    """

    def __init__(self, table_name):
        """
        Initializes the DynamoDB client.

        Args:
            table_name (str): The name of the DynamoDB table.

        """
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def set(self, key, value, ttl=None):
        """
        Save or overwrite a value in the cache with an optional TTL.

        Args:
            key (str): The cache key under which the value is stored.
            value (str or dict): The value to be stored.
            ttl (int, optional): The time-to-live (TTL) in seconds. If provided,
                the item will expire and be deleted after this duration.

        """
        item = {"id": key, "value": json.dumps(value)}

        if ttl:
            ttl_epoch = int(time.time()) + ttl
            item["ttl"] = ttl_epoch

        self.table.put_item(Item=item)

    def get(self, key, **kwargs):
        """
        Retrieve a value from the cache.

        Args:
            key (str): The cache key.

        Returns:
            The retrieved value, or None if the key does not exist.
            If the value was stored as a JSON string, it will be returned as a dict.

        """
        try:
            response = self.table.get_item(Key={"id": key})

            if "Item" in response:
                return json.loads(response["Item"]["value"])

            return None
        except ClientError as e:
            self.logger.exception(e.response["Error"]["Message"])
            return None

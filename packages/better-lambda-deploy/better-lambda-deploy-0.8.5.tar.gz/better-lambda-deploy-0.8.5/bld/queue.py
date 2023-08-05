import boto3
import simplejson as json
import os
import queue
import bld


ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
APPLICATION = os.getenv("APPLICATION")


class Queue(object):
    """
    An SQS queue. Any objects that inherit from this class will automatically be
    deployed as SQS queues.

    TODO: Maybe somehow add a message structure somehow, so that messages added to the
    queue can be validated against it?
    """

    def __init__(self):
        self.queue_name = (
            APPLICATION + "-" + self.__class__.__name__.lower() + "-" + bld.get_env()
        )
        print(f"Environment: {ENVIRONMENT}")
        self.environment = ENVIRONMENT
        if self.environment == "sam":
            print("Using localstack for queues.")
            endpoint_url = "http://localstack:4566"
            self.client = boto3.client(
                "sqs", region_name="us-east-1", endpoint_url=endpoint_url
            )
        elif self.environment == "local":
            print("Using localhost for queues.")
            endpoint_url = "http://localhost:4566"
            self.client = boto3.client(
                "sqs", region_name="us-east-1", endpoint_url=endpoint_url
            )
        else:
            self.client = boto3.client("sqs")

        if not self.environment == "local":
            self.queue_url = self.client.get_queue_url(QueueName=self.queue_name)[
                "QueueUrl"
            ]
        else:
            # Initialize a local queue.
            self.local_queue = queue.SimpleQueue()

    def add_message(self, message, trigger_time=None):
        """
        Add a message to the queue.
        """
        if not self.environment == "local":
            res = self.client.send_message(
                QueueUrl=self.queue_url, MessageBody=json.dumps(message)
            )
            print(res)
        else:
            self.local_queue.put(message)

    def change_message_visibility(self, receipt_handle, visibility_timeout):
        res = self.client.change_message_visibility(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle,
            VisibilityTimeout=visibility_timeout,
        )
        print(res)

    def delete_message(self, receipt_handle):
        res = self.client.delete_message(
            QueueUrl=self.queue_url, ReceiptHandle=receipt_handle
        )
        print(res)

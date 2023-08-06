import boto3
import json
import logging

logger = logging.getLogger("microgue")


class QueueConnectionFailed(Exception):
    pass


class DeleteFailed(Exception):
    pass


class AbstractQueue:
    queue = None
    queue_url = ""

    def __init__(self, *args, **kwargs):
        logger.debug(f"########## {self.__class__.__name__} __init__ ##########")
        logger.debug(f"AbstractQueue.queue: {AbstractQueue.queue}")
        try:
            if AbstractQueue.queue is None:
                logger.debug("connecting to sqs")
                AbstractQueue.queue = boto3.client("sqs")
            else:
                logger.debug("using existing connection to sqs")
        except Exception as e:
            raise QueueConnectionFailed(str(e))

    def send(self, message):
        logger.debug(f"########## {self.__class__.__name__} Send ##########")
        if type(message) is dict:
            message = json.dumps(message)
        try:
            self.queue.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message
            )
        except Exception as e:
            logger.error(f"########## {self.__class__.__name__} Send Failed")
            logger.error(f"{e.__class__.__name__}: {str(e)}")
            return False
        return True

    def receive(self, max_number_of_messages=1, visibility_timeout=1, wait_time=1):
        logger.debug(f"########## {self.__class__.__name__} Receive ##########")
        logger.debug(f"max_number_of_messages: {max_number_of_messages}")
        logger.debug(f"visibility_timeout: {visibility_timeout}")
        logger.debug(f"wait_time: {wait_time}")
        response = self.queue.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_number_of_messages,
            VisibilityTimeout=visibility_timeout,
            WaitTimeSeconds=wait_time
        )
        logger.debug(f"response: {response}")
        response_messages = response.get("Messages", [])
        messages = []
        for i in range(len(response_messages)):
            try:
                message = {
                    "id": response_messages[i]["ReceiptHandle"],
                    "message": json.loads(response_messages[i]["Body"])
                }
                messages.append(message)
            except:
                pass
        return messages

    def delete(self, message):
        logger.debug(f"########## {self.__class__.__name__} Delete ##########")
        logger.debug(f"message: {message}")

        try:
            self.queue.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message.get("id")
            )
        except Exception as e:
            logger.error(f"########## {self.__class__.__name__} Delete Failed")
            logger.error(f"{e.__class__.__name__}: {str(e)}")
            raise DeleteFailed(str(e))

        return True

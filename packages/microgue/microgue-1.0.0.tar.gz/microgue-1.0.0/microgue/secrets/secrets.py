import boto3
import json
import logging

logger = logging.getLogger("microgue_secrets")


class GetSecretFailed(Exception):
    pass


class SecretsConnectionFailed(Exception):
    pass


class Secrets:
    secrets = None

    def __init__(self, *args, **kwargs):
        logger.debug(f"########## {self.__class__.__name__} __init__ ##########")
        logger.debug(f"Secrets.secrets: {Secrets.secrets}")
        try:
            if Secrets.secrets is None:
                logger.debug("connecting to secretsmanager")
                Secrets.secrets = boto3.client("secretsmanager")
            else:
                logger.debug("using existing connection to secretsmanager")
        except Exception as e:
            raise SecretsConnectionFailed(str(e))

    def get_secret(self, secret_name):
        logger.debug(f"########## {self.__class__.__name__} Get Secret ##########")
        logger.debug(f"secret_name: {secret_name}")
        try:
            get_secret_value_response = self.secrets.get_secret_value(
                SecretId=secret_name
            )
        except Exception as e:
            raise GetSecretFailed(str(e))
        return json.loads(get_secret_value_response["SecretString"])

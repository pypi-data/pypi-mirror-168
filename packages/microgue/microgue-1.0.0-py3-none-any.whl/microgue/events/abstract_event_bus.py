import boto3
import json
import logging

logger = logging.getLogger("microgue")


class AbstractEventBus:
    event_bus = None
    event_bus_name = None
    event_bus_region = None
    event_source = None

    def __init__(self, *args, **kwargs):
        logger.debug(f"########## {self.__class__.__name__} __init__ ##########")
        logger.debug(f"AbstractEventBus.event_bus: {AbstractEventBus.event_bus}")
        if AbstractEventBus.event_bus is None:
            logger.debug("connecting to eventbridge")
            AbstractEventBus.event_bus = boto3.client(service_name="events", region_name=self.event_bus_region)
        else:
            logger.debug("using existing connection to eventbridge")

    def publish(self, event_type, event_data={}):
        logger.debug(f"########## {self.__class__.__name__} Publish ##########")
        logger.debug(f"event_type: {event_type}")
        logger.debug(f"event_data: {event_data}")

        response = self.event_bus.put_events(
            Entries=[{
                "Source": self.event_source,
                "DetailType": event_type,
                "Detail": json.dumps(event_data),
                "EventBusName": self.event_bus_name
            }]
        )

        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return True
        else:
            logger.critical(f"{self.__class__.__name__} - publish - failed")
            return False

import abc
import logging
from typing import Optional

from boto3 import client
from google.protobuf.any_pb2 import Any
from google.protobuf.json_format import MessageToJson
from google.protobuf.message import Message
from google.protobuf.timestamp_pb2 import Timestamp
from parrotschemas.events_monitoring.v1.events_pb2 import (
    ERROR,
    NORMAL,
    Event,
    EventType,
    Header,
)

logger = logging.getLogger(__name__)


PREFIX = 'parrotschemas'


class Publisher(abc.ABC):
    @abc.abstractmethod
    def publish(self, correlation_id: str, event: Message, silent: bool) -> None:
        """Called when publishing an event."""
        raise NotImplementedError


class KinesisPublisher(Publisher):
    def __init__(self, stream_name: str, region_name: str = "us-east-1", endpoint_url: Optional[str] = None):
        if endpoint_url is not None:
            self._client = client("kinesis", region_name=region_name, endpoint_url=endpoint_url)
        else:
            self._client = client("kinesis", region_name=region_name)

        self.stream_name = stream_name

    def publish_error(self, correlation_id: str, event: Message, silent: bool = False) -> None:
        self._publish(correlation_id, event, silent, ERROR)

    def publish(self, correlation_id: str, event: Message, silent: bool = False) -> None:
        self._publish(correlation_id, event, silent, NORMAL)

    def _publish(self, correlation_id: str, event: Message, silent: bool, type_: EventType) -> None:
        if isinstance(event, Event):
            raise ValueError("Type Event is not allowed to be published directly!")

        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        any_event = Any()
        any_event.Pack(event)

        # +1 for "."
        event_type = event.DESCRIPTOR.full_name[len(PREFIX) + 1 :]

        publish_event = Event(
            header=Header(
                event_type=event_type,
                correlation_id=correlation_id,
                timestamp=timestamp,
                silent=silent,
            ),
            spec=any_event,
            type=type_,
        )
        key = any_event.type_url
        try:
            self._client.put_record(
                StreamName=self.stream_name,
                PartitionKey=correlation_id,
                Data=MessageToJson(
                    message=publish_event,
                    indent=None,  # type: ignore
                    preserving_proto_field_name=True,
                ).encode('utf-8'),
            )
        except Exception:
            logger.exception(f"Failed to publish record to Kinesis stream {self.stream_name} with key {key}.")

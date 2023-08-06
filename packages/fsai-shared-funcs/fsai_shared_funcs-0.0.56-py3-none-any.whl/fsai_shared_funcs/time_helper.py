from datetime import datetime
from beartype import beartype
from google.protobuf.timestamp_pb2 import Timestamp


def get_datetime_from_pb_ts(timestamp):
    return datetime.fromtimestamp(timestamp.seconds + timestamp.nanos / 1e9)


@beartype
def get_pb_ts_from_datetime(python_timestamp: datetime) -> Timestamp:
    t = python_timestamp.timestamp()
    return Timestamp(seconds=int(t), nanos=int(t % 1 * 1e9))

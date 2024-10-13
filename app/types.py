import asyncio
from typing import Literal, NamedTuple, TypeAlias, TypedDict, Union

TypeQueue: TypeAlias = Union[
                        asyncio.Queue,
                        asyncio.LifoQueue,
                        asyncio.PriorityQueue,
]

StateTrafficLights: TypeAlias = Literal['red', 'yellow', 'green']


class StreamTraffic(TypedDict):
    """Пешеход или автомобиль. Указываем на каком светофоре находится"""
    uid_tf_lights: int
    type_tr: Literal['auto', 'walker']


class CommonSizesQueue(NamedTuple):
    size: int
    uids: list[int]

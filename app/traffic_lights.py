import asyncio
from typing import Literal, NoReturn, TypeAlias, Union

from app.types import StateTrafficLights, TypeQueue

TrafficLightType: TypeAlias = Union[
                                'TrafficLightsCar',
                                'TrafficLightsWalker',
                                'TrafficLightsBase']


class TrafficLightsBase:
    def __init__(self,
                 traffic_light_id: int,
                 name: str,
                 type_tr_lights: Literal['auto', 'walker'],
                 state: StateTrafficLights,
                 queue: TypeQueue,
                 related_possible: tuple,
                 related_impossible: tuple) -> None:
        self.uid = traffic_light_id
        self.name = name
        self.type_tr_lights = type_tr_lights
        self.state = state
        self.queue = queue
        self.related_possible = related_possible
        self.related_impossible = related_impossible
        self.signal_time_opetaion: int = 0
        self.last_state: StateTrafficLights = state

    def change_state(self, state: StateTrafficLights) -> None:
        self.last_state = self.state
        self.state = state
        self.signal_time_opetaion = 0

    async def update_signal_time(self) -> NoReturn:
        while True:
            await asyncio.sleep(1)
            self.signal_time_opetaion += 1


class TrafficLightsWalker(TrafficLightsBase):
    pass


class TrafficLightsCar(TrafficLightsBase):
    pass

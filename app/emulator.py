import asyncio
import random
from typing import TYPE_CHECKING

from app.config import MAX_COUNT_PER_ITERATION, TYPE_LOAD_TRAFFIC
from app.exceptions import NotFoundLoadTrafficError
from app.traffic_lights import TrafficLightType
from app.types import StreamTraffic

if TYPE_CHECKING:
    from main import TrafficController


class OrganizationMovement:
    def __init__(
            self,
            traffic_lights: dict[int, TrafficLightType],
            controller: 'TrafficController') -> None:
        self.traffic_lights = traffic_lights
        self.controller = controller

    def move_car(self) -> int:
        cars_left = 0
        for tr_lights in self.traffic_lights.values():
            if tr_lights.state != 'green':
                continue

            count_car = 0
            while count_car < MAX_COUNT_PER_ITERATION:
                try:
                    tr_lights.queue.get_nowait()
                    cars_left += 1
                except asyncio.QueueEmpty:
                    break
                count_car += 1
        return cars_left

    def get_traffic_1k1(self) -> list[StreamTraffic]:
        traffic = []
        for tr_light in self.traffic_lights.values():
            if random.choice((False, True)):
                traffic.append(StreamTraffic(
                            uid_tf_lights=tr_light.uid,
                            type_tr=tr_light.type_tr_lights)
                )
        return traffic

    def get_traffic_2k1(self) -> list[StreamTraffic]:
        traffic = []
        for tr_light in self.traffic_lights.values():
            if random.choice((False, True)):
                traffic.append(StreamTraffic(
                            uid_tf_lights=tr_light.uid,
                            type_tr=tr_light.type_tr_lights)
                )
                traffic.append(StreamTraffic(
                    uid_tf_lights=tr_light.uid,
                    type_tr=tr_light.type_tr_lights)
                )

        return traffic

    def get_traffic_1k2(self) -> list[StreamTraffic]:
        traffic = []
        tr_light = list(self.traffic_lights.values())
        random.shuffle(tr_light)
        for tr_light in tr_light[:len(tr_light)//2]:
            if random.choice((False, True)):
                traffic.append(StreamTraffic(
                            uid_tf_lights=tr_light.uid,
                            type_tr=tr_light.type_tr_lights)
                )
        return traffic

    def get_traffic(self) -> list[StreamTraffic]:
        match TYPE_LOAD_TRAFFIC:
            case '1k1':
                return self.get_traffic_1k1()
            case '1k2':
                return self.get_traffic_1k2()
            case '2k1':
                return self.get_traffic_2k1()
            case _:
                raise NotFoundLoadTrafficError(
                    f'Данный тип эмуляции не найден ({TYPE_LOAD_TRAFFIC})'
                    )

    async def put_traffic(self, traffic: list[StreamTraffic]) -> None:
        for entity in traffic:
            await self.traffic_lights[
                entity['uid_tf_lights']].queue.put(entity)

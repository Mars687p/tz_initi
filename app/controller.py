import asyncio
from typing import Callable

from app.config import TIME_PER_ITERATION
from app.traffic_lights import TrafficLightType
from app.types import CommonSizesQueue


class TrafficController:
    def __init__(
            self,
            traffic_lights: dict[int, TrafficLightType]
                                                    ) -> None:
        self.traffic_lights = traffic_lights

    async def set_sending_timer(self, sec: int | float,
                                func: Callable, *args) -> None:
        await asyncio.sleep(sec)
        func(*args)

    async def start_time_tracking(self) -> None:
        asyncio.gather(*(tr_light.update_signal_time()
                         for tr_light in self.traffic_lights.values()))

    async def get_common_qsizes(self) -> list[CommonSizesQueue]:
        """
            Получаем наибольшую очередь для светофоров.
            При наличии связанного светофора, например два для одного
            пешеходного перехода, мы суммируем их очереди.
            Также добавляем коомбинации с пешеходными переходами
        """
        longest_queues: list[CommonSizesQueue] = []
        passed_queue_for_walker: set[int] = set()
        for tr_light in self.traffic_lights.values():
            # фильтруем дубликаты для пешеходных светофоров
            if tr_light.type_tr_lights == 'walker':
                if tr_light.uid in passed_queue_for_walker:
                    continue
                passed_queue_for_walker.add(tr_light.uid)
                passed_queue_for_walker.add(tr_light.related_possible[0])

            size = tr_light.queue.qsize()

            max_rel_size = self._max_qsize_of_possible_combinations(
                                tr_light.related_possible)

            uids: list[int] = [tr_light.uid]
            if max_rel_size is not None:
                size += max_rel_size[1]
                if type(max_rel_size[0]) is tuple:
                    uids.extend(max_rel_size[0])
                elif type(max_rel_size[0]) is int:
                    uids.append(max_rel_size[0])

            longest_queues.append(
                        CommonSizesQueue(
                            size=size,
                            uids=uids
                            )
                )
        return sorted(longest_queues, reverse=True)

    def _max_qsize_of_possible_combinations(
                        self,
                        rel_possible: tuple) -> tuple[tuple | int, int] | None:
        """
            Находим максимальную возможную коомбаницию
            со связанными светофорами
        """
        max_rel_size: tuple[tuple | int, int] | None = None
        for related in rel_possible:
            currnet_size = 0
            if type(related) is int:
                currnet_size = self.traffic_lights[
                                    related].queue.qsize()
            else:
                currnet_size = self._get_total_qsize_for_walkers_lights(
                                            related[0])

            if not max_rel_size or max_rel_size[1] < currnet_size:
                max_rel_size = (related, currnet_size)
        return max_rel_size

    async def evaluate_load_tr_lights(
                            self,
                            size_queue: CommonSizesQueue) -> None:
        """
            Оцениваем нагрузку на предмет самой длинной очереди.
            Если для самой длинной очереди не включен зеленый свет, то включаем
        """
        if size_queue.size == 0:
            return
        rel_tr_lights = [self.traffic_lights[i] for i in size_queue.uids]
        passed_uid: set[int] = set()
        for tr_light in rel_tr_lights:
            self.change_state_yellow_tr_light(tr_light)
            if (tr_light.state in ['green', 'yellow']):
                continue

            passed_uid.add(tr_light.uid)
            if tr_light.state == 'red':
                self.turn_signal_state(tr_light, passed_uid)

    def turn_signal_state(self,
                          tr_light: TrafficLightType,
                          passed_uid: set[int]) -> None:
        """
            Включаем зеленый для целевого светофора и выключаем
            для тех, которые не могут работать вместе с ним.
        """
        if tr_light.type_tr_lights == 'auto':
            tr_light.change_state('yellow')
        else:
            tr_light.change_state('green')

        for rel_uid in tr_light.related_impossible:
            rel_light = self.traffic_lights[rel_uid]
            if rel_light.uid in passed_uid:
                continue

            if rel_light.type_tr_lights == 'auto':
                if rel_light.state == 'red':
                    continue
                rel_light.change_state('yellow')
                passed_uid.add(rel_light.uid)

            else:
                passed_uid.add(rel_light.uid)
                asyncio.create_task(self.set_sending_timer(
                                            TIME_PER_ITERATION-0.1,
                                            rel_light.change_state, 'red'))

    def check_yellow_state(self) -> None:
        for tr_light in self.traffic_lights.values():
            if tr_light.state == 'yellow':
                self.change_state_yellow_tr_light(tr_light)

    def change_state_yellow_tr_light(self, tr_light: TrafficLightType) -> None:
        if tr_light.state == 'yellow':
            if tr_light.last_state == 'green':
                tr_light.change_state('red')
            else:
                tr_light.change_state('green')

    def _get_total_qsize_for_walkers_lights(self, uid: int) -> int:
        """ Пешеходные светофоры - спаренные, т.к. нет ситуаций,
            где они могли бы включаться/выключаться отдельно
        """
        tr_light = self.traffic_lights[uid]
        rel_tr_light = self.traffic_lights[tr_light.related_possible[0]]
        return tr_light.queue.qsize() + rel_tr_light.queue.qsize()

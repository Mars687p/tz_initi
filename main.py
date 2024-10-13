import asyncio
from contextlib import suppress
from typing import NoReturn

from app.config import TIME_PER_ITERATION
from app.controller import TrafficController
from app.emulator import OrganizationMovement
from tests.test_case import TEST_STREAM_TRAFFIC, TRAFFIC_LIGHTS


async def start() -> NoReturn:
    controller = TrafficController(TRAFFIC_LIGHTS)
    move_emulator = OrganizationMovement(TRAFFIC_LIGHTS, controller)
    asyncio.create_task(controller.start_time_tracking())  # type: ignore

    # test_case
    traffic = TEST_STREAM_TRAFFIC
    await move_emulator.put_traffic(traffic)

    count_iter = 0
    total_add = 0
    total_released = 0
    while True:
        traffic = move_emulator.get_traffic()
        await move_emulator.put_traffic(traffic)
        controller.check_yellow_state()
        load_list = await controller.get_common_qsizes()
        cars_left = move_emulator.move_car()
        await controller.evaluate_load_tr_lights(load_list[0])

        for tr_light in TRAFFIC_LIGHTS.values():
            print(tr_light.name, tr_light.state, tr_light.uid)
        for item in load_list:
            print(item)

        count_iter += 1
        total_add += len(traffic)
        total_released += cars_left
        conversion = 0.0
        with suppress(ZeroDivisionError):
            conversion = round(total_released/total_add*100, 2)

        print(f'\n{count_iter=} | Добавлено в очередь {len(traffic)} | ',
              f'Вычтено из очереди {cars_left} |\n',
              f'Всего: выпущено={total_released}, +={total_add}',
              f'{conversion=}%\n')

        await asyncio.sleep(TIME_PER_ITERATION)


if __name__ == '__main__':
    asyncio.run(start())

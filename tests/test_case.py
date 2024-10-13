import asyncio

from app.traffic_lights import (TrafficLightsCar, TrafficLightsWalker,
                                TrafficLightType)
from app.types import StreamTraffic

TRAFFIC_LIGHTS: dict[int, TrafficLightType] = {
    1: TrafficLightsCar(traffic_light_id=1,
                        name='Автомобильный: верхний',
                        type_tr_lights='auto',
                        state='green',
                        queue=asyncio.Queue(),
                        related_possible=(3, (7, 8)),
                        related_impossible=(2, 4, 5, 6, 9, 10, 11, 12),
                        ),

    2: TrafficLightsCar(traffic_light_id=2,
                        name='Автомобильный: правый',
                        type_tr_lights='auto',
                        state='red',
                        queue=asyncio.Queue(),
                        related_possible=(4, (9, 10)),
                        related_impossible=(1, 3, 5, 6, 7, 8, 11, 12),
                        ),

    3: TrafficLightsCar(traffic_light_id=3,
                        name='Автомобильный: нижний',
                        type_tr_lights='auto',
                        state='red',
                        queue=asyncio.Queue(),
                        related_possible=(1, (11, 12)),
                        related_impossible=(2, 4, 5, 6, 7, 8, 9, 10),
                        ),

    4: TrafficLightsCar(traffic_light_id=4,
                        name='Автомобильный: левый',
                        type_tr_lights='auto',
                        state='red',
                        queue=asyncio.Queue(),
                        related_possible=(2, (5, 6)),
                        related_impossible=(1, 3, 7, 8, 9, 10, 11, 12),
                        ),

    5: TrafficLightsWalker(traffic_light_id=5,
                           name='Пешеходный: верхний левый',
                           type_tr_lights='walker',
                           state='red',
                           queue=asyncio.Queue(),
                           related_possible=(6,),
                           related_impossible=(1, 2, 3),
                           ),

    6: TrafficLightsWalker(traffic_light_id=6,
                           name='Пешеходный: верхний правый',
                           type_tr_lights='walker',
                           state='red',
                           queue=asyncio.Queue(),
                           related_possible=(5,),
                           related_impossible=(1, 2, 3),
                           ),

    7: TrafficLightsWalker(traffic_light_id=7,
                           name='Пешеходный: правый верхний',
                           type_tr_lights='walker',
                           state='green',
                           queue=asyncio.Queue(),
                           related_possible=(8,),
                           related_impossible=(2, 3, 4),
                           ),

    8: TrafficLightsWalker(traffic_light_id=8,
                           name='Пешеходный: правый нижний',
                           type_tr_lights='walker',
                           state='green',
                           queue=asyncio.Queue(),
                           related_possible=(7,),
                           related_impossible=(2, 3, 4),
                           ),

    9: TrafficLightsWalker(traffic_light_id=9,
                           name='Пешеходный: нижний левый',
                           type_tr_lights='walker',
                           state='red',
                           queue=asyncio.Queue(),
                           related_possible=(10,),
                           related_impossible=(1, 3, 4),
                           ),

    10: TrafficLightsWalker(traffic_light_id=10,
                            name='Пешеходный: нижний правый',
                            type_tr_lights='walker',
                            state='red',
                            queue=asyncio.Queue(),
                            related_possible=(9,),
                            related_impossible=(1, 3, 4),
                            ),

    11: TrafficLightsWalker(traffic_light_id=11,
                            name='Пешеходный: левый нижний',
                            type_tr_lights='walker',
                            state='red',
                            queue=asyncio.Queue(),
                            related_possible=(12,),
                            related_impossible=(1, 2, 4),
                            ),

    12: TrafficLightsWalker(traffic_light_id=12,
                            name='Пешеходный: левый верхний',
                            type_tr_lights='walker',
                            state='red',
                            queue=asyncio.Queue(),
                            related_possible=(11,),
                            related_impossible=(1, 2, 4),
                            ),
    }

# 4 машины сверху, 2 машины снизу, 3 машины слева, 0 справа
# 4 пешехода сверху(с разных сторон), 4 пешехода слева, 4 пешехода справа
TEST_STREAM_TRAFFIC: list[StreamTraffic] = [
    # автомобили: верх
    StreamTraffic(uid_tf_lights=1, type_tr=TRAFFIC_LIGHTS[1].type_tr_lights),
    StreamTraffic(uid_tf_lights=1, type_tr=TRAFFIC_LIGHTS[1].type_tr_lights),
    StreamTraffic(uid_tf_lights=1, type_tr=TRAFFIC_LIGHTS[1].type_tr_lights),
    StreamTraffic(uid_tf_lights=1, type_tr=TRAFFIC_LIGHTS[1].type_tr_lights),

    # автомобили: низ
    StreamTraffic(uid_tf_lights=3, type_tr=TRAFFIC_LIGHTS[3].type_tr_lights),
    StreamTraffic(uid_tf_lights=3, type_tr=TRAFFIC_LIGHTS[3].type_tr_lights),

    # автомобили: лево
    StreamTraffic(uid_tf_lights=4, type_tr=TRAFFIC_LIGHTS[4].type_tr_lights),
    StreamTraffic(uid_tf_lights=4, type_tr=TRAFFIC_LIGHTS[4].type_tr_lights),
    StreamTraffic(uid_tf_lights=4, type_tr=TRAFFIC_LIGHTS[4].type_tr_lights),

    # пешеходы: верх
    StreamTraffic(uid_tf_lights=5, type_tr=TRAFFIC_LIGHTS[5].type_tr_lights),
    StreamTraffic(uid_tf_lights=5, type_tr=TRAFFIC_LIGHTS[5].type_tr_lights),
    StreamTraffic(uid_tf_lights=5, type_tr=TRAFFIC_LIGHTS[5].type_tr_lights),
    StreamTraffic(uid_tf_lights=6, type_tr=TRAFFIC_LIGHTS[6].type_tr_lights),

    # пешеходы: лево
    StreamTraffic(uid_tf_lights=11, type_tr=TRAFFIC_LIGHTS[11].type_tr_lights),
    StreamTraffic(uid_tf_lights=11, type_tr=TRAFFIC_LIGHTS[11].type_tr_lights),
    StreamTraffic(uid_tf_lights=12, type_tr=TRAFFIC_LIGHTS[12].type_tr_lights),
    StreamTraffic(uid_tf_lights=12, type_tr=TRAFFIC_LIGHTS[12].type_tr_lights),

    # пешеходы: право
    StreamTraffic(uid_tf_lights=7, type_tr=TRAFFIC_LIGHTS[7].type_tr_lights),
    StreamTraffic(uid_tf_lights=7, type_tr=TRAFFIC_LIGHTS[7].type_tr_lights),
    StreamTraffic(uid_tf_lights=7, type_tr=TRAFFIC_LIGHTS[7].type_tr_lights),
    StreamTraffic(uid_tf_lights=7, type_tr=TRAFFIC_LIGHTS[7].type_tr_lights),
]

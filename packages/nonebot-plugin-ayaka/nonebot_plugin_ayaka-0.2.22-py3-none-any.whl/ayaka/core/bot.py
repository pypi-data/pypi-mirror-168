from asyncio import sleep
import asyncio
from time import time
from ayaka.adapter import Bot, on_connect
from .model import Ayaka


ayaka = Ayaka()


@on_connect
async def add_ayakabot(bot: Bot):
    ayaka.add(bot)

    # 执行定时任务
    abot = ayaka.get_abot(bot.self_id)
    while True:
        time_i = int(time())
        for dev in abot.devices:
            for app in dev.apps:
                if app.valid:
                    for t in app.timers:
                        if t.check(time_i):
                            await t.run()

        await sleep(1)

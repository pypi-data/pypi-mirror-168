from typing import TYPE_CHECKING
from ayaka.adapter import logger

if TYPE_CHECKING:
    from .plugin import AyakaApp


class AyakaTimer:
    def __init__(self, app: "AyakaApp", loop, start, func) -> None:
        self.app = app
        self.loop = loop
        self.func = func
        self.start = start
        self.next = start

    def check(self, time_i):
        if time_i >= self.next:
            self.next = time_i + self.loop - ((time_i - self.next) % self.loop)
            return True

    def clone(self, app: "AyakaApp"):
        t = AyakaTimer(app, self.loop, self.start, self.func)
        return t

    async def run(self):
        # 上 下 文 切 换
        self.app.switch(self.func)

        logger.info(
            f"触发Ayaka应用[<y>{self.app.name}</y>] <y>定时任务</y>")
        await self.func()

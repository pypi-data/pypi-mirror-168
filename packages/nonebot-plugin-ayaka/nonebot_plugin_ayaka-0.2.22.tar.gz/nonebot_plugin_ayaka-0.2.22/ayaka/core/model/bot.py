import asyncio
from typing import List
from .device import AyakaDevice
from ayaka.adapter import Bot


class AyakaBot:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.devices: List[AyakaDevice] = []
        self.update = None
        asyncio.create_task(self.update_dev())

    async def update_dev(self):
        if not self.update:
            self.update = asyncio.create_task(self._update_dev())
        await self.update
        self.update = None

    async def _update_dev(self):
        # 自动增加
        data = await self.bot.get_group_list()
        g_ids = [d["group_id"] for d in data]

        data = await self.bot.get_friend_list()
        p_ids = [d["user_id"] for d in data]

        ids = g_ids + p_ids

        # 删除失效的
        self.devices = [d for d in self.devices if d in ids]

        # 新增缺失的
        g_ids = list(
            set(g_ids) - set(d.device_id for d in self.devices if d.group))
        p_ids = list(
            set(p_ids) - set(d.device_id for d in self.devices if not d.group))

        for id in g_ids:
            d = AyakaDevice(self, id, True)
            self.devices.append(d)

        for id in p_ids:
            d = AyakaDevice(self, id, False)
            self.devices.append(d)

    def _get_device(self, device_id: int):
        for d in self.devices:
            if d.device_id == device_id:
                return d

    async def get_device(self, device_id: int):
        '''获取设备'''
        d = self._get_device(device_id)
        if not d:
            await self.update_dev()
            d = self._get_device(device_id)

        return d

    async def is_friend(self, uid: int):
        data = await self.bot.get_friend_list()
        for d in data:
            if uid == d["user_id"]:
                return True
        return False

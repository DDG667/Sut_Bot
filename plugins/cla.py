

class qqid:
    def __init__(self,main,event,bot):
        self.gid=event.group_id
        self.uid=event.get_user_id()
        self.evt=event
        self.bot=bot
        self.main=main
    async def getage(self):
        await self.bot.get_stranger_info(user_id=self.uid,no_cache=True)
    async def getname(self):
        await self.bot.get_stranger_info(user_id=self.uid,no_cache=True)
    async def ban(self,time):
        await self.bot.set_group_ban(group_id=self.gid,user_id=self.uid,duration=time)





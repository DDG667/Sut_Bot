import re
import aiohttp
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot import on_command,on_regex
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me


test = on_command("test", permission=SUPERUSER)


@test.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    for i in (await bot.call_api('get_group_root_files',group_id=551099482))['files']:
        await bot.call_api('delete_group_file',group_id=551099482,file_id=i['file_id'],busid=i['busid'])
        print(i)
    await test.finish('Ok')

m=on_command('&#91;QUICK MATH&#93;')
@m.handle()
async def _(e:GroupMessageEvent):
    await m.finish('答案：'+str(eval(e.get_plaintext().replace('[QUICK MATH] ','').replace(' = ?',''))))
'''
o=on_regex('.*?第.题.*?',rule=to_me())
@o.handle()
async def _(e:GroupMessageEvent):
    async with aiohttp.ClientSession() as aio:
        b=re.findall('【(.*?)】',e.get_plaintext())[0]
        t=await(await aio.get(f'https://m.gushiwen.cn/search.aspx?value={b}',allow_redirects=True)).text()
        r=re.findall(rf'<span style="color:#B00815">{b}</span>[，|？](.*?)[。？]',t)[0]
        await o.finish(MessageSegment.at(e.user_id)+MessageSegment.text(r))
'''

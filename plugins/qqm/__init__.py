from requests import get
from json import loads
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageSegment, Message


headers = {'Referer': 'https://i.y.qq.com/'}
qqm = on_command('qqt')


@qqm.handle()
async def _(event: GroupMessageEvent):
    name = event.get_plaintext().replace('qqt ', '')
    n = name.split(' ')
    l = n[-1]
    name = ''
    for i in n[0:-1]:
        name += i
    with get(f'https://shc.y.qq.com/soso/fcgi-bin/search_for_qq_cp?_&format=json&w={name}&n={l}', headers=headers) as b:
        x = '        Sut - 请选择'
        y = 0
        global z
        z = {}
        for i in loads(b.text[9:-1])['data']['song']['list']:
            y += 1
            x += f"\n{y} - {i['songname']}"
            z[str(y)] = i['songmid']
        await qqm.send(x)


@qqm.got('id')
async def _(args: Message = CommandArg()):
    id = args.extract_plain_text()
    i = loads(get('http://ovooa.com/API/QQ_Music/?id='+z[id]).text)
    url = i["data"]["music"]
    with get(url) as a:
        await qqm.send(MessageSegment.record(a.content))
        await qqm.finish('嗯哼~我可是高性能的机器人哦')

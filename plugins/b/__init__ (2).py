from json import loads
from requests import get
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, ActionFailed, MessageSegment, NetworkError

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}


async def gn(name, l):
    r = get(
        f'http://music.163.com/api/search/get/?&s={name}&limit={l}&type=1&offset=0')
    global j
    j = '      ATRI - 请选择'
    global h
    h = {}
    global a
    a = 1
    for i in loads(r.text)['result']['songs']:
        j += f"\n{a} - {i['name']}\n        -  {i['artists'][0]['name']} "
        h.setdefault(str(a), i['id'])
        a += 1
    r.close()
    await t163.send(j)
    


async def na(n):
    try:
        if len(n.split(' ')) > 1:
            global l
            l = int(n.split(' ')[-1])
            global name
            name = ''
            for i in n.split(' ')[0:-1]:
                name += i
        else:
            name = n
            l = 1/0
    except Exception:
        l = 10

t163 = on_command('163t')


@t163.handle()
async def m2(matcher: Matcher, event: GroupMessageEvent, args: Message = CommandArg()):
    global name
    name = event.get_plaintext().replace('163t', '')
    if name != '':
        matcher.set_arg("name", args)


@t163.got('name', prompt='能不能告诉ATRI你想听的音乐的名字?')
async def m3(event: GroupMessageEvent):
    global name
    name = event.get_plaintext().replace('163t ', '').replace('163t', '')
    await na(name)
    await gn(name, l)


@t163.receive()
async def m4(event: GroupMessageEvent):
    try:
        id = h[event.get_plaintext()]
        try:
            with get(f'http://music.163.com/song/media/outer/url?id={id}.mp3') as a:
                await m163.send(MessageSegment.record(a.content))
            await t163.finish()#'嗯哼~我可是高性能的机器人哦')
        except ActionFailed:
            await t163.finish(Message('ATRI无法获取此音乐的数据，请检查是否需要VIP才能播放，或者联系维护人员[CQ:face,id=106]'))
        except NetworkError:
            await t163.send('请耐心等待...')
        except KeyError:
            await t163.finish()
    except KeyError:
        await t163.finish('请输入数字！')

m163 = on_command('163')


@m163.handle()
async def m1(event: GroupMessageEvent):
    await m163.send(Message('因为是把音乐下载后再发送的，所以延迟有点高，请耐心等待。[CQ:face,id=319]'))
    name = ''
    for i in str(event.original_message).split(" ")[1:]:
        name += i
    try:
        r = get(
            f'http://music.163.com/api/search/get/?&s={name}&limit=1&type=1&offset=0')
        r.close()
        id = str(loads(r.text)['result']['songs'][0]['id'])
        url=f'http://music.163.com/song/media/outer/url?id={id}.mp3'
        #r=get(url)
        #if r.status_code==404:
        try:
            with get(url) as a:
                await m163.send(MessageSegment.record(a.content))
                a.close()
        except ActionFailed:
            await m163.finish(Message('ATRI无法获取此音乐的数据，请检查是否需要VIP才能播放，或者联系维护人员[CQ:face,id=106]'))
        await m163.finish()
    except NetworkError:
        await m163.send('请耐心等待...')

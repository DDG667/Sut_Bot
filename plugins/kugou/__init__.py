from json import loads
from nonebot import on_command
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.cqhttp import MessageSegment
import aiohttp


async def search(keyword: str) -> list[list[str]]:
    api = "http://mobilecdn.kugou.com/api/v3/search/song"
    async with aiohttp.ClientSession() as r:
        a = await r.get(f"{api}?keyword={keyword}&pagesize={10}")
        data = loads(await a.text())["data"]["info"]
        info = [[], [], []]
        for i in data:
            info[0].append(i["songname"])
            info[1].append(i["hash"])
            info[2].append(i["singername"])
        return info


async def geturl(hash: str) -> str:
    api = f"http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={hash}"
    async with aiohttp.ClientSession() as r:
        a = await r.get(api)
        url = loads(await a.text())["url"]
        return url


kugou = on_command("kugou")


@kugou.handle()
async def _(msg: GroupMessageEvent):
    txt = "\t\t\t\t\t- Sut -"
    name = msg.get_plaintext().replace("kugou ", "")
    global info
    info = await search(name)
    for i, j, ij in zip(range(len(info[0])), info[0], info[2]):
        txt += f"\n{i+1} - {j}\n\t\t\t\t- {ij}"
    await kugou.send(txt)


@kugou.receive()
async def _(msg: GroupMessageEvent):
    try:
        id = int(msg.get_plaintext()) - 1
    except TypeError:
        await kugou.finish()
    hash = info[1][id]
    url = await geturl(hash)
    async with aiohttp.ClientSession() as r:
        b = await (await r.get(url)).read()
    await kugou.finish(MessageSegment.record(b))

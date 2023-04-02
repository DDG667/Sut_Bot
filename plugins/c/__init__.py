from re import findall
from json import loads
from nonebot.permission import SUPERUSER
from nonebot import on_command
from nonebot.adapters.cqhttp import Message, MessageEvent, MessageSegment, message
from nonebot.adapters.onebot.v11 import GroupMessageEvent
import aiohttp


def getid(event):
    msg = str(event.original_message)
    uid = findall("\[CQ:at,qq=(.*?)\]", msg)[0]
    return uid


def all(surl, a, b):
    uid = getid(b)
    url = f"http://ovooa.com/API{surl}?QQ={uid}"
    return a.finish(Message(f"[CQ:image,file={url}]"))


mo = on_command("膜拜")


@mo.handle()
async def _(event: GroupMessageEvent):
    surl = "/face_worship/"
    await all(surl, mo, event)


mom = on_command("摸")


@mom.handle()
async def _(event: GroupMessageEvent):
    surl = "/face_petpet/"
    await all(surl, mom, event)


yao = on_command("嗦")


@yao.handle()
async def _(event: GroupMessageEvent):
    surl = "/face_suck/"
    await all(surl, yao, event)


dao = on_command("捣")


@dao.handle()
async def _(event: GroupMessageEvent):
    surl = "/face_pound/"
    await all(surl, dao, event)


wan = on_command("玩")


@wan.handle()
async def _(event: GroupMessageEvent):
    surl = "/face_play/"
    await all(surl, wan, event)


pai = on_command("拍")


@pai.handle()
async def _(event: GroupMessageEvent):
    surl = "/face_pat/"
    await all(surl, pai, event)


ken = on_command("啃")


@ken.handle()
async def _(event: GroupMessageEvent):
    surl = "/face_bite/"
    await all(surl, ken, event)


si = on_command("撕")


@si.handle()
async def _(event: GroupMessageEvent):
    surl = "/si/"
    await all(surl, si, event)


yi = on_command("祭")


@yi.handle()
async def _(event: GroupMessageEvent):
    surl = "/yi/"
    await all(surl, yi, event)


kchi = on_command("吃")


@kchi.handle()
async def _(event: GroupMessageEvent):
    surl = "/chi/"
    await all(surl, kchi, event)


zha = on_command("炸")


@zha.handle()
async def _(event: GroupMessageEvent):
    surl = "/face_yu/"
    await all(surl, zha, event)


pa = on_command("爬")


@pa.handle()
async def _(event: GroupMessageEvent):
    surl = "/pa/"
    await all(surl, pa, event)


diu = on_command("丢")


@diu.handle()
async def _(event: GroupMessageEvent):
    surl = "/diu/"
    await all(surl, diu, event)


tian = on_command("舔")


@tian.handle()
async def _(event: GroupMessageEvent):
    id = getid(event)
    url = f"http://ovooa.com/API/tian/?url=http://q1.qlogo.cn/g?b=qq&nk={id}&s=640"
    await tian.finish(Message(f"[CQ:image,file={url}]"))


async def direct(a, url):
    with get(url) as b:
        await a.finish(b.text)


dongm = on_command("动漫一言")


@dongm.handle()
async def _():
    url = "http://ovooa.com/API/dmyiyan/api.php"
    await direct(dongm, url)


qingh = on_command("情话")


@qingh.handle()
async def _():
    url = "http://ovooa.com/API/qing/api.php"
    await direct(qingh, url)


tu = on_command("一图", permission=SUPERUSER)


@tu.handle()
async def _():
    async with aiohttp.ClientSession() as r:
        a = await r.get("http://ovooa.com/API/Pximg")
        data = loads(await a.text())["data"]
        title = MessageSegment.text(data["title"])
        author = MessageSegment.text(data["author"])
        url = data["urls"]["original"].replace("https", "http")
        async with aiohttp.ClientSession() as r:
            a = await r.get(url=url)
            await tu.finish(
                title
                + MessageSegment.image(await a.read())
                + MessageSegment.text("作者：")
                + author
            )


from PIL import Image, ImageDraw
from .draw import draw

luxun = on_command("鲁迅说")


@luxun.handle()
async def _(event: MessageEvent):
    await luxun.finish(
        MessageSegment.image(draw(event.get_plaintext().replace("鲁迅说", "")))
    )

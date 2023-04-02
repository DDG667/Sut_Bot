#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 3.10

from ..w import wiki
from ..func import send
from re import findall
from json import loads
from requests import get, post
from . import linuxcommands
from urllib.parse import quote_plus
from nonebot import on_command
from nonebot.adapters.cqhttp import GroupMessageEvent, Message




# WARNING: Decompyle incomplete

wp = on_command("维基百科")


@wp.handle()
async def _(event: GroupMessageEvent):
    word = event.get_plaintext().replace("维基百科 ", "")
    global w
    w = wiki(word)
    global res
    res = w.search()
    msg = "    Sut - Wikipedia"
    for i, j in zip(range(len(res)), res):
        msg += f"\n{i+1} - {j}"
    await wp.send(msg)


# WARNING: Decompyle incomplete


@wp.receive("1")
async def w2(event: GroupMessageEvent):
    try:
        id = int(event.get_plaintext()) - 1
        global cho
        cho = res[id]
        summary = w.summary(cho)
        await send(wp, summary)
    except ValueError:
        await wp.finish("请输入数字！")


# WARNING: Decompyle incomplete


@wp.receive("2")
async def _(event: GroupMessageEvent):
    if "详细" in event.get_plaintext():
        longmsg = w.page(cho).content
        await send(wp, longmsg)
        await wp.finish()
    await wp.finish()


linuxc = on_command("LinuxCMD")


@linuxc.handle()
async def _():
    msg = "  Sut - Linux Command"
    global listc
    listc = [i for i in dir(linuxcommands) if i[0] != "_"]
    for i, j in zip(range(len(listc)), listc):
        msg += f"\n{i+1} - {j}"
    await linuxc.finish(msg)


dongman = on_command("动漫")


@dongman.handle()
async def _(event: GroupMessageEvent):
    url = findall("\[CQ:image.*?url=(.*?);is_", str(event.get_message()))[0]
    api='https://api.trace.moe/search?anilistInfo'
    with open('./a.jpeg','wb') as a:
        a.write(get(url).content)
    with post(
        url=api,data=open('./a.jpeg','rb'),headers={"Content-Type": "image/jpeg"}
    ) as a:
        data = a.json()
        if data["error"] != "":
            print(data)
            await dongman.finish("Failed!")
        msg = "    Sut"
        res = data["result"]
        for i in res:
            if i["anilist"]["isAdult"]:
                await dongman.send("跳过成人内容一个")
                continue
            msg += f'\n- {i["anilist"]["title"]["native"]} ({i["anilist"]["title"]["english"]})\n\tSimilarity:\n\t{i["similarity"]*100}%\n\tImage:[CQ:image,file={i["image"]}]'
            await dongman.send(
                f'{i["anilist"]["title"]["native"]} ({i["anilist"]["title"]["english"]})\nVideo:'
            )
            await dongman.send(Message(f'[CQ:video,file={i["video"]}]'))
        a.close()
        await dongman.finish(Message(msg))

from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    ActionFailed,
    MessageSegment,
    NetworkError,
)
import os
import re
import httpx
from PIL import Image,ImageDraw,ImageFont,ImageColor
current_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".") + "/"
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}


async def gn(name, l) -> None:
    async with httpx.AsyncClient() as b:
        r = await b.get(
            url=f"http://music.163.com/api/search/get/?&s={name}&limit={l}&type=1&offset=0",
            timeout=3000,
        )
    global j
    j = "      ATRI - 请选择"
    global h
    h = {}
    global a
    a = 1
    for i in r.json()["result"]["songs"]:
        j += f"\n{a} - {i['name']}        -  {i['artists'][0]['name']} "
        h.setdefault(str(a), i["id"])
        a += 1
    im=Image.open(f'{current_path}bg.jpg')
    ImageDraw.Draw(im).text((32,32),j,font=ImageFont.truetype(f'{current_path}font.ttf',200))
    im.save(f'{current_path}1.jpg')
    await t163.send(MessageSegment.image(open(f'{current_path}1.jpg','rb').read()))


async def na(n) -> None:
    try:
        if len(n.split(" ")) > 1:
            global l
            l = int(n.split(" ")[-1])
            global name
            name = ""
            for i in n.split(" ")[0:-1]:
                name += i
        else:
            name = n
            raise ZeroDivisionError
    except ZeroDivisionError:
        l = 10


t163 = on_command("163t")


@t163.handle()
async def m2(
    matcher: Matcher, event: GroupMessageEvent, args: Message = CommandArg()
) -> None:
    global name
    name = event.get_plaintext().replace("163t", "")
    if name != "":
        matcher.set_arg("name", args)


@t163.got("name", prompt="能不能告诉ATRI你想听的音乐的名字?")
async def m3(event: GroupMessageEvent) -> None:
    global name
    name = event.get_plaintext().replace("163t ", "").replace("163t", "")
    await na(name)
    await gn(name, l)


@t163.receive()
async def m4(event: GroupMessageEvent) -> None:
    try:
        try:
            id = h[event.get_plaintext()]
        except KeyError:
            await t163.finish('错误选项！')
        try:
            url = f"http://music.163.com/song/media/outer/url?id={id}.mp3"
            async with httpx.AsyncClient() as r:
                await t163.finish(
                    MessageSegment.record(
                        (
                            await r.get(url=url, follow_redirects=True, timeout=15000)
                        ).read()
                    )
                )
        except ActionFailed:
            await t163.finish(
                Message("ATRI无法获取此音乐的数据，请检查是否需要VIP才能播放，或者联系维护人员[CQ:face,id=106]")
            )
        except NetworkError:
            await t163.send("请耐心等待...")
        except KeyError:
            await t163.finish()
        except httpx.ConnectError:
            await c163.send("连接错误，摆烂")
        except httpx.ConnectTimeout:
            await c163.send("连接超时，摆烂")
    except KeyError:
        await t163.finish("请输入数字！")


m163 = on_command("163")


@m163.handle()
async def m1(event: GroupMessageEvent) -> None:
    await m163.send(Message("因为是把音乐下载后再发送的，所以延迟有点高，请耐心等待。[CQ:face,id=319]"))
    name = ""
    for i in str(event.original_message).split(" ")[1:]:
        name += i
    try:
        async with httpx.AsyncClient() as a:
            r = await a.get(
                url=f"http://music.163.com/api/search/get/?&s={name}&limit=1&type=1&offset=0",
                timeout=3000,
            )
        id = str(r.json()["result"]["songs"][0]["id"])
        url = f"http://music.163.com/song/media/outer/url?id={id}.mp3"
        try:
            async with httpx.AsyncClient() as r2:
                await m163.send(
                    MessageSegment.record(
                        (
                            await r2.get(url=url, follow_redirects=True, timeout=15000)
                        ).read()
                    )
                )
        except ActionFailed:
            await m163.send(
                Message("ATRI无法获取此音乐的数据，请检查是否需要VIP才能播放，或者联系维护人员[CQ:face,id=106]")
            )
    except NetworkError:
        await m163.send("请耐心等待...")
    except httpx.ConnectError:
        await c163.send("连接错误，摆烂")
    except httpx.ConnectTimeout:
        await c163.send("连接超时，摆烂")
    except ActionFailed:
        await c163.send("发送失败，摆烂")
    finally:
        await c163.finish()


c163 = on_command("163c")


@c163.handle()
async def m5(
    matcher: Matcher, event: GroupMessageEvent, args: Message = CommandArg()
) -> None:
    global name
    name = event.get_plaintext().replace("163t", "")
    if name != "":
        matcher.set_arg("name", args)


@c163.got("name", prompt="能不能告诉ATRI音乐的名字?")
async def m6(event: GroupMessageEvent) -> None:
    global name
    name = event.get_plaintext().replace("163c ", "").replace("163c", "")
    await na(name)
    await gn(name, l)


@c163.receive()
async def m7(event: GroupMessageEvent, bot: Bot) -> None:
    try:
        id = h[event.get_plaintext()]
    except KeyError:
        await c163.finish('错误选项！')
    async with httpx.AsyncClient() as r:
        try:
            j = (
                await r.get(
                    url=f"http://music.163.com/api/song/lyric?id={id}+&lv=1&tv=-1",
                    timeout=3000,
                )
            ).json()
            nk = (
                event.sender.nickname if isinstance(event.sender.nickname, str) else " "
            )
            m = [
                #    MessageSegment.node_custom(
                #        event.user_id,
                #        nk,
                #        Message(
                #            MessageSegment.record(
                #                (
                #                    await r.get(
                #                        url=f"http://music.163.com/song/media/outer/url?id={id}.mp3",
                #                        timeout=15000,
                #                        follow_redirects=True,
                #                    )
                #                ).read()
                #            )
                #        ),
                #    )
            ]
            for i in re.findall("](.*?)\n", j["lrc"]["lyric"]):
                if i == "":
                    continue
                m.append(MessageSegment.node_custom(event.user_id, nk, i))
            await bot.send_group_forward_msg(group_id=event.group_id, messages=m)
        except KeyError:
            await c163.send("未找到内容，摆烂")
        except httpx.ConnectError:
            await c163.send("连接错误，摆烂")
        except httpx.ConnectTimeout:
            await c163.send("连接超时，摆烂")
        except ActionFailed:
            await c163.send("发送失败，摆烂")
        except Exception:
            await c163.send('未知错误，摆大烂')
        finally:
            await c163.finish()

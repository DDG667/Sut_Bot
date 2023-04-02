from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment, Bot
import aiohttp
import re
from random import randint, sample

N = 1

url = "https://yande.re/post?tags={}"

yande = on_command("yande")


@yande.handle()
async def _(event: GroupMessageEvent, bot: Bot):
    try:
        async with aiohttp.ClientSession() as r:
            key = (
                r"order%3Arandom"
                if event.get_plaintext().replace("yande", "") in ["", " "]
                else event.get_plaintext().replace("yande ", "").replace(" ", "_")
            )
            a = await bot.get_stranger_info(user_id=event.user_id)
            t = await r.get(url.format(key))
            open("/sdcard/Python/a.html", "wb").write(await t.read())
            u = f"""https://yande.re/post?page={randint(1,int(re.findall(f'aria-label="Page (.*?)"', await t.text())[-1]))}&tags={key}"""
            print(u)
            r = await r.get(u)
            l = re.findall('"file_url":"(.*?)"', await r.text())
            m = [
                MessageSegment.node_custom(
                    event.user_id, "Sut的舔狗", f'我承认，我 {a["nickname"]} ，就是Sut的舔狗。'
                )
            ]
            for i in sample(l, N):
                m.append(
                    MessageSegment.node_custom(
                        event.user_id,
                        "Sut的舔狗",
                        Message(f"[CQ:image,file={i},url={i}]"),
                    )
                )
            await bot.send_group_forward_msg(
                messages=m, group_id=event.group_id, time_out=60
            )
    except Exception as e:
        print(e)
        await yande.send("未知错误，懒得处理")
    finally:
        await yande.finish()

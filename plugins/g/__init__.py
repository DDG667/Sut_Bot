import re
import subprocess
import asyncio
from typing import SupportsAbs
from nonebot import logger, on_fullmatch, on_command, on_notice, on_regex
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    GroupBanNoticeEvent,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
)
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER, SuperUser
import json
import os
import random
import hashlib

from nonebot.rule import is_type, to_me

path = (
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")
    + "/"
)
ud = on_fullmatch("update data", permission=SUPERUSER)


@ud.handle()
async def _(bot: Bot):
    ids_names = {
        i["group_id"]: {
            "name": i["group_name"],
            "member": [
                j["user_id"]
                for j in await bot.get_group_member_list(group_id=i["group_id"])
            ],
        }
        for i in await bot.get_group_list()
    }
    jsons = json.dumps(ids_names)
    with open(f"{path}test.json", "w") as a:
        a.write(jsons)
    await ud.finish("OK")


get = on_command("sget", permission=SUPERUSER)


@get.handle()
async def _(event: MessageEvent):
    msg = "查询到此人在以下群聊"
    try:
        id = int(event.get_plaintext().replace("sget ", ""))
        with open(f"{path}test.json", "r") as a:
            jsons: dict = json.loads(a.read())
        for i, j in jsons.items():
            if id in j["member"]:
                msg += f'\n{j["name"]}({i})'
    except ValueError:
        msg = "参数错误！"
    await get.finish(msg)


allb = on_command("s_ban", permission=SUPERUSER)


@allb.handle()
async def _(event: MessageEvent, bot: Bot):
    success = "以下群聊禁言成功\n"
    fail = "\n以下群聊禁言失败"
    try:
        id = int(event.get_plaintext().replace("s_ban", ""))
        with open(f"{path}test.json", "r") as a:
            jsons: dict = json.loads(a.read())
        for i, j in jsons.items():
            if id in j["member"]:
                try:
                    await bot.set_group_ban(group_id=int(i), user_id=id)
                    success += f'{j["name"]}({i})\n'
                except ActionFailed:
                    fail += f'\n{j["name"]}({i})'
                    continue
        msg = success + fail
    except ValueError:
        msg = "参数错误"
    await allb.finish(msg)


allub = on_command("s_unban", permission=SUPERUSER)


@allub.handle()
async def _(event: MessageEvent, bot: Bot):
    success = "以下群聊解禁成功\n"
    fail = "\n以下群聊解禁失败"
    try:
        id = int(event.get_plaintext().replace("s_unban", ""))
        with open(f"{path}test.json", "r") as a:
            jsons: dict = json.loads(a.read())
        for i, j in jsons.items():
            if id in j["member"]:
                try:
                    await bot.set_group_ban(group_id=int(i), user_id=id, duration=0)
                    success += f'{j["name"]}({i})\n'
                except ActionFailed:
                    fail += f'\n{j["name"]}({i})'
                    continue
        msg = success + fail
    except ValueError:
        msg = "参数错误"
    await allub.finish(msg)


sview = on_fullmatch("sview", permission=SUPERUSER)


@sview.handle()
async def _(bot: Bot):
    isnum = ismem = isgem = 0
    with open(f"{path}test.json", "r") as a:
        jsons: dict = json.loads(a.read())
        islen = len(jsons)
        for i, j in jsons.items():
            ismem += len(j["member"])
            if (
                await bot.get_group_member_info(
                    group_id=int(i), user_id=int(bot.self_id), no_cache=True
                )
            )["role"] != "member":
                isnum += 1
                isgem += len(j["member"])
    await sview.finish(
        f"Sut 已加入 {islen} 个群聊，总人数 {ismem} 人，当上了 {isnum} 个群的管理，管辖 {isgem} 人。"
    )


ssay = on_command("ssay")


@ssay.handle()
async def _(event: MessageEvent, bot: Bot):
    msg = event.get_plaintext().replace("ssay ", "")
    with open(f"{path}test.json", "r") as a:
        for i in json.loads(a.read()):
            if i in {"768176998", "645320692", "483245347", "569764861", "374500473"}:
                continue
            r = hashlib.md5(str(random.random()).encode()).hexdigest()
            try:
                await bot.send_group_msg(
                    group_id=int(i),
                    message=Message(f"--[机器人广播]--\n\n{msg}\n\n<-- {r[8:24]} -->"),
                )
                await asyncio.sleep(0.1)
            except Exception:
                continue
    await ssay.finish("OK")


def issu(bot: Bot, qq: int) -> bool:
    if str(qq) in bot.config.superusers:
        return True
    return False


"""
whotmatme=on_command('0')
@whotmatme.handle()
async def _(bot:Bot,event:MessageEvent):
    if issu(bot,findall('\[CQ:at,qq=(.*?)\]',str(event.original_message))[0]):
        await whotmatme.finish('1')
    else:
        await whotmatme.finish('2')
"""


n = on_fullmatch(".", permission=SUPERUSER)


@n.handle()
async def _():
    for i in range(0, 29):
        await n.send(Message("[CQ:at,qq=3499074683]快女装！"))
    await n.finish(Message("[CQ:at,qq=3499074683]快女装！"))


s = on_command("bash", permission=SUPERUSER)


@s.handle()
async def _(event: GroupMessageEvent):
    cmd = event.get_plaintext()[5:]
    await s.finish(subprocess.getoutput(cmd))


"""
sjqmp=on_fullmatch('随机个签')
@sjqmp.handle()
async def _(event:GroupMessageEvent,bot:Bot):
    for i in await bot.get_group_member_list(group_id=event.group_id):
        a=await bot.get(user_id= i['user_id'],no_cache=False)

    await sjqmp.finish(str(a))
"""
"""
o=on_fullmatch('..',permission=SUPERUSER)
@o.handle()
async def _(bot:Bot):
    await bot.call_api('upload_private_file',user_id=2187784548,file='/storage/emulated/0/Python/d/b.zip',name='b.zip')
    await o.finish()
"""

o = on_notice(rule=is_type(GroupBanNoticeEvent))


@o.handle()
async def _(bot: Bot, event: GroupBanNoticeEvent):
    if str(event.user_id) in bot.config.superusers and event.duration != 0:
        try:
            await bot.set_group_ban(
                group_id=event.group_id, user_id=event.user_id, duration=0
            )
        except ActionFailed as a:
            print(a)
    await o.finish()


ll = on_regex(pattern=".*?你.*?主人.*?", rule=to_me())


@ll.handle()
async def _():
    await ll.finish("QQ：3580426231")

sh = on_command("骰子", permission=SUPERUSER)


@sh.handle()
async def _(args: Message = CommandArg()):
    await sh.finish(Message(f"[CQ:dice,value={args.extract_plain_text()}]"))


shu = on_command("fakenode", permission=SUPERUSER)


@shu.handle()
async def _(event: GroupMessageEvent, bot: Bot):
    inf = re.findall("(.*)：(.*)", event.get_plaintext())

    messages = []
    for i in inf:
        messages.append(
            MessageSegment.node_custom(
                i[0], (await bot.get_stranger_info(user_id=i[0]))["nickname"], i[-1]
            )
        )
    await bot.send_group_forward_msg(
        messages=messages,
        group_id=event.group_id,
    )
    print(messages)
    await shu.finish()


# w=on_command('跨群聊天')

caidan = on_fullmatch(".菜单")


@caidan.handle()
async def _():
    await caidan.finish("开发中...")

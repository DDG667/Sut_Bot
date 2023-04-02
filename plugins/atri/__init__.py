# /usr/bin/python3
# coding: utf-8
import io
import os
import qrcode
from re import findall
from nonebot.adapters.cqhttp import Message, Bot
from nonebot.permission import SUPERUSER
from nonebot.rule import is_type
from requests import get
from .a import msg
from loguru import logger
from nonebot import load_from_toml, on_notice
from random import choice
from json import loads
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    GROUP,
    GroupUploadNoticeEvent,
    MessageSegment,
    NoticeEvent,
    NotifyEvent,
)
from nonebot.plugin import on_command
from .data import V_PATH, I_PATH, M_PATH, current_path

__plugin_name__ = "ATRI 语音包"
__usage__ = "atri"

atri = on_command("ATRI", permission=GROUP, priority=50)


@atri.handle()
async def _():
    with open(f"{V_PATH}{choice(os.listdir(V_PATH))}", "rb") as a:
        await atri.finish(MessageSegment.record(a.read()))


DM = on_command("- ATRI -", aliases={"-ATRI-"}, permission=GROUP, priority=50)


@DM.handle()
async def _():
    a = 0
    b = " " * 12 + "- ATRI -"
    for i in os.listdir(M_PATH):
        a += 1
        b += f"\n{a} - {i}"
    logger.info(b)
    await DM.send(b)


@DM.got("id")
async def _(event: GroupMessageEvent):
    try:
        id = int(str(event.original_message))
    except ValueError:
        await DM.finish("请输入数字！")
    id = int(str(event.original_message))
    with open(M_PATH + os.listdir(M_PATH)[id - 1], "rb") as a:
        await DM.finish(MessageSegment.record(a.read()))


CPDD = on_command("CPDD~", aliases={"CPDD", "cpdd"}, permission=GROUP, priority=50)


@CPDD.handle()
async def _():
    with open(I_PATH + choice(os.listdir(I_PATH)), "rb") as a:
        await CPDD.finish(MessageSegment.image(a.read()))


chat_notice = on_notice(rule=is_type(GroupUploadNoticeEvent))
ccc = on_notice(rule=is_type(NotifyEvent))


@ccc.handle()
@chat_notice.handle()
async def handle_first_receive(bot: Bot, notice: NoticeEvent):
    j = loads(notice.json())
    if j["notice_type"] == "notify" and j["target_id"] == 2849425197:
        await chat_notice.finish(choice(msg))
    elif j["notice_type"] == "group_upload" and j["group_id"] in {686221881,581659285,551099482}:
        un = loads(
            str(
                await bot.get_stranger_info(user_id=j["user_id"], no_cache=True)
            ).replace("'", '"')
        )["nickname"]
        file = j["file"]
        fn, fs, fu = file["name"], file["size"], file["url"]
        buf=io.BytesIO()
        qr=qrcode.QRCode(version=1,box_size=100)
        qr.add_data(fu)
        qr.make_image().save(buf)
        await chat_notice.finish(
            Message(f"{un} 上传了文件 {fn}  ({fs} b)"+MessageSegment.image(buf)+"尽量不要使用QQ扫描")
        )
    if j["group_id"] == 582489481:
        await chat_notice.finish(notice.json())
    await chat_notice.finish()


leave = on_command("走吧", permission=SUPERUSER)


@leave.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await leave.send("诸位，再见。")
    await bot.set_group_leave(group_id=event.group_id, is_dismiss=True)
    await leave.finish()


clean = on_command("clean", permission=SUPERUSER)


@clean.handle()
async def _(bot: Bot):
    await bot.clean_cache()

    await clean.finish("Done!")


update = on_command("Update", permission=SUPERUSER)


@update.handle()
async def _():
    load_from_toml(current_path + "../../pyproject.toml")
    await update.finish("Successfully!")

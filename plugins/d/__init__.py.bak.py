import os
from random import randint
from time import localtime
from json import loads, dumps
from pickle import load, dump
from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from classes import users

path = (
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")
    + "/"
)


def get_data() -> users:
    with open(f"{path}pydata", "rb") as data:
        return load(data)


def get_num() -> int:
    with open(f"{path}cf.json", "r") as cf:
        return len(loads(cf.read())[str(localtime()[7])])


def cf_add(id: int) -> None:
    with open(f"{path}cf.json", "r") as cf:
        dict = loads(cf.read())
        dict[str(localtime()[7])].append(str(id))
    with open(f"{path}cf.json", "w") as cf:
        cf.write(dumps(dict))


def save_data(us: users) -> None:
    with open(f"{path}pydata", "wb") as data:
        dump(us, data)


checkin = on_fullmatch("签到")


@checkin.handle()
async def _(event: GroupMessageEvent):
    if randint(1, 99) < 11:
        await checkin.finish(Message(f"[CQ:at,qq={event.user_id}]\n签到失败！（快去买彩票）"))
    id = event.user_id
    num = 40 if get_num() > 40 else get_num()
    rint = randint(0, 50 - num)
    us = get_data()
    us[id].achange_score(rint)
    cf_add(id)
    save_data(us)
    await checkin.finish(Message(f"[CQ:at,qq={id}]\n签到成功！积分加 {rint}\n你是今天第 {num} 个签到的"))

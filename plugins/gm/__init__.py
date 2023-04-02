import os
from json import loads
from random import randint
from re import findall
from nonebot import on_command, on_notice, on_request
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    ActionFailed,
    GroupRequestEvent,
    Message,
    GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent,
    MessageSegment,
)
from nonebot.adapters.onebot.v11.event import GroupRequestEvent
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from nonebot.rule import is_type,to_me

current_path = (
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")
    + "/"
)
G = [686221881, 600973599, 681048214, 551099482, 582489481, 768176998, 581659285]
# mulu = on_command('菜单')
ban = on_command("禁", priority=1, block=True, permission=SUPERUSER | GROUP_OWNER)
jie = on_command("解", priority=1, block=True, permission=SUPERUSER | GROUP_OWNER)
ban_all = on_command("ALL", permission=SUPERUSER | GROUP_OWNER, priority=1, block=True)
kick = on_command("踢", permission=SUPERUSER | GROUP_OWNER)
anyso = on_command("群名", permission=SUPERUSER | GROUP_OWNER)
setad = on_command("管", permission=SUPERUSER | GROUP_OWNER)
toux = on_command("头衔")
ran_ban = on_command("禁言抽奖", priority=1, block=True)
welcom = on_notice(rule=is_type(GroupIncreaseNoticeEvent))


# @mulu.handle()
# async def mulu_handle():
#    await mulu.finish(f'                    Sut\n--如果不能用是因为你未获得权限--\n一言 一句 一图 语录 毒汤 舔狗 笑话 头像 天气 聊天 动漫图 土味情话\n短网址(dwzcn) IP QR\nSut  (随机一条Sut语音)\n戳一戳 （随机Sut语录）\nCPDD(70中随机Sut图片)\nDM  (send Dear Moments)\nLATS  (send Light Across the Seas)\n163\\163t\\qqt 歌名 (语音发送音乐)\n群管功能:\n        禁  解  踢  抽  管+/-  ALL\n--———————————--\nPS:发送指令即可查看\n例如:官方群\n开发兼维护：3580426231')


# ban = on_command('禁', priority=1, block=True,permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
def nnn(event, ban):
    gid = event.group_id
    msg = str(event.original_message)
    uids = findall("\[CQ:at,qq=(.*?)\]", msg)
    at = ""
    ch = "你们"
    if len(uids) == 1:
        ch = "你"
    for uid in uids:
        at += f"[CQ:at,qq={uid}]"
    if ban:
        time = msg.split(" ")[-1]
        try:
            eval(time)
        except SyntaxError:
            time = "300"
        finally:
            return gid, uids, eval(time), at, ch
    return gid, uids, at, ch


@ban.handle()
async def ban_handle(bot: Bot, event: GroupMessageEvent):
    gid, uids, time, at, ch = nnn(event, ban=True)
    try:
        for uid in uids:
            await bot.set_group_ban(group_id=gid, user_id=uid, duration=time)
        await ban.finish(Message(f"{at}{ch}被禁言 {time} 秒"))
    except ActionFailed:
        await ban.finish(Message("权限不足[CQ:face,id=106]"))
    except ValueError:
        pass


# jie = on_command('解', priority=1, block=True,permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@jie.handle()
async def jie_handle(bot: Bot, event: GroupMessageEvent):
    gid, uids, at, ch = nnn(event, ban=False)
    for uid in uids:
        await bot.set_group_ban(group_id=gid, user_id=uid, duration=0)
    await ban.finish(Message(f"{at}{ch}已被解除禁言"))


# ban_all = on_command('ALL', permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)


@ban_all.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = event.get_message()
    enable = not (" " in str(msg))
    try:
        await bot.set_group_whole_ban(group_id=event.group_id, enable=bool(enable))
        if enable:
            await ban_all.finish("Sut已开启全员禁言")
        else:
            await ban_all.finish("Sut已关闭全员禁言")
    except ActionFailed:
        await ban_all.finish(Message("[CQ:face,id=106]权限不足"))


@setad.handle()
async def sead(bot: Bot, event: GroupMessageEvent):
    gid, uids, at, ch = nnn(event, False)
    if len(uids) == 0:
        await setad.finish("你还没有@任何人呢")
    a = "+" in str(event.original_message)
    for uid in uids:
        try:
            await bot.set_group_admin(group_id=gid, user_id=uid, enable=a)
        except ActionFailed:
            await setad.finish(Message("[CQ:face,id=106]权限不足"))
    if a:
        await setad.finish(Message(f"{at}恭喜{ch}成为管理员！"))
    else:
        await setad.finish()


@toux.handle()
async def touxi(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    t = args.extract_plain_text()
    await bot.call_api('set_group_special_title',group_id=event.group_id,user_id=event.user_id,special_title=t,duration=-1)
    await toux.finish()

@ran_ban.handle()
async def ran_dan_handle(
    bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()
):
    group_id = event.group_id
    userid = event.get_user_id()
    if args.extract_plain_text() != "":
        time = randint(1, int(args.extract_plain_text()))
        if time > 2591999:
            await ran_ban.finish("时长过长")
    else:
        time = randint(1, 300)
    try:
        await bot.set_group_ban(group_id=group_id, user_id=int(userid), duration=time)
        await ban.finish(Message(f"[CQ:at,qq={userid}]你被禁言 {time} 秒"))
    except ActionFailed:
        await ban.finish(Message("权限不足[CQ:face,id=106]"))


@welcom.handle()
async def welcome(event: GroupIncreaseNoticeEvent):
    user = event.get_user_id()
    at_ = "[CQ:at,qq={}]".format(user)
    msg = at_ + "欢迎大佬加入"
    if event.group_id in G:
        await welcom.send(
            Message(f"[CQ:image,file=http://q1.qlogo.cn/g?b=qq&nk={user}&s=640]{msg}")
        )
        await welcom.finish("年纪轻轻就进了这个群，你的未来指定是寄了")


tuich = on_notice(rule=is_type(GroupDecreaseNoticeEvent))


@tuich.handle()
async def tuichu(event: GroupDecreaseNoticeEvent):
    user = event.get_user_id()
    msg = "{}退出了群聊".format(user)
    if event.group_id in G:
        await tuich.finish(
            Message(f"[CQ:image,file=http://q1.qlogo.cn/g?b=qq&nk={user}&s=640]{msg}")
        )


# kick = on_command('踢', permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@kick.handle()
async def kickh(bot: Bot, event: GroupMessageEvent):
    gid, uids, _, _ = nnn(event=event, ban=False)
    msg = ""
    try:
        for uid in uids:
            await bot.set_group_kick(
                group_id=gid, user_id=uid, reject_add_request=False
            )
            msg += f"{uid}\n"
    except ActionFailed:
        await kick.finish(Message("权限不足[CQ:face,id=106]"))
    await kick.finish(f"{msg}已被踢出群聊")


# anyso=on_command('群名',permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@anyso.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    gid = event.group_id
    name = args.extract_plain_text()
    try:
        await bot.set_group_name(group_id=gid, group_name=name)
    except ActionFailed:
        await anyso.finish(Message("权限不足[CQ:face,id=106]"))
    await anyso.finish(f"Sut已将群名改为 {name}")


say = on_command("say ", permission=SUPERUSER, priority=3)


@say.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    try:
        gid = int(args.extract_plain_text().split(" ")[-1])
        msg = args.extract_plain_text().split(" ")[0]
    except TypeError:
        gid = event.group_id
        msg = args.extract_plain_text()
    finally:
        await bot.send_group_msg(group_id=int(gid), message=msg, auto_escape=False)
        await say.finish("发送成功")


@say.handle()
async def _(bot: Bot, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    gid = str(msg.split(" ")[-1])
    msg = msg.split(" ")[0]
    await bot.send_group_msg(group_id=int(gid), message=msg, auto_escape=False)
    await say.finish("发送成功")


che = on_command("¹", permission=SUPERUSER)


@che.handle()
async def _(event: GroupMessageEvent, bot: Bot):
    id = findall(",id=(.*?)\]", loads(event.json())["raw_message"])[0]
    await bot.delete_msg(message_id=int(id))
    await che.finish()


c = on_request()


@c.handle()
async def _(event: GroupRequestEvent, bot: Bot):
    await c.send(f"    入群申请\n来自：{event.user_id}\n{event.comment}")
    b = on_command("", permission=SUPERUSER | GROUP_OWNER, rule=to_me())

    @b.handle()
    async def _(even: GroupMessageEvent):
        while True:
            if str(even.user_id) in bot.config.superusers:
                if "y" in even.get_plaintext():
                    await event.approve(bot)
                else:
                    await event.reject(bot, even.get_plaintext())
                break
        await b.finish()

    await c.finish()


t = on_command("退出", permission=SUPERUSER)


@t.handle()
async def _(event: GroupMessageEvent, bot: Bot):
    try:
        a = int(event.get_plaintext()[3:])
        await bot.send_group_msg(group_id=a, message="【Warning】\nSut将退出本群！！")
        await bot.send_group_msg(
            group_id=a,
            message=Message(f"虽然很舍不得，但毕竟是命令……各位下次再见啦！")+MessageSegment.image(f'{current_path}leave.jpg'),
        )
        await bot.set_group_leave(group_id=a)
        await t.finish("已退出")
    except ActionFailed:
        await t.finish("退出失败")
    except IndexError:
        await t.finish("参数错误")





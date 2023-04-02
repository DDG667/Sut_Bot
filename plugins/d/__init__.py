import os
import json
from random import randint
from re import findall
from time import localtime
from nonebot import on_command
from nonebot.adapters.cqhttp import Message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.exception import ActionFailed
from nonebot.permission import SUPERUSER



current_path = os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + os.path.sep + ".") + "/"


guize=on_command('签到积分规则')
@guize.handle()
async def _():
    await guize.finish('设今天为第n个签到\n    则获得积分为随机1到51-n\n    如果最大随机数小于10，则为10')

checkin = on_command('签到')

@checkin.handle()
async def _(event: GroupMessageEvent):
    uid = str(event.user_id)
    day = str(localtime()[7])
    with open(f'{current_path}cf.json', 'r') as a:
        dic = json.loads(a.read())
        if uid in dic[day]:
            await checkin.finish(Message(f'[CQ:at,qq={uid}]\n一天只能签到一次！'))
        else:
            dic[day].append(uid)
            p=len(dic[day])
            m=51-p
            if m<10:
                m=10
            score = randint(1, m)
            with open(f'{current_path}cf.json', 'w') as a:
                a.write(json.dumps(dic))

            if randint(1,100)>10:
                with open(f'{current_path}score.json', 'r') as b:
                    ddd = json.loads(b.read())
                    try:
                        ddd[uid] += score
                    except KeyError:
                        ddd[uid]=score
                    finally:
                        with open(f'{current_path}score.json', 'w') as b:
                            b.write(json.dumps(ddd))
                            await checkin.finish(Message(f'[CQ:at,qq={uid}]\n签到成功！积分+{score}\n你是今天第{p}个签到的'))
    await checkin.finish(Message(f'[CQ:at,qq={uid}]签到失败！明天再来吧\n(快去买彩票)'))

schange=on_command('积分更改',permission=SUPERUSER)
@schange.handle()
async def _(event:GroupMessageEvent):
#    try:
        at=findall('qq=(.*?)\]',str(event.get_message()))[0]
        sc=event.get_plaintext().split(' ')[-1]
        with open(f'{current_path}score.json','r') as a:
            dic=json.loads(a.read())
            dic[at]=int(sc)
        with open(f'{current_path}score.json','w') as b:
            b.write(json.dumps(dic))
        await schange.finish('修改成功！')
#    except Exception:
baihang = on_command('积分排行')


@baihang.handle()
async def _(bot: Bot):
    with open(f'{current_path}score.json', 'r') as a:
        d = json.loads(a.read())
    uid=list(d.keys())
    sco=list(d.values())
    for i in range(len(sco)-1):
        c=sco[i:]
        n=c.index(max(c))+i
        sco[n],sco[i]=sco[i],sco[n]
        uid[n],uid[i]=uid[i],uid[n]
    e = ' '*10+'Sut - 签到积分'
    for n,i,j in zip(range(len(sco)),uid,sco):
        g = json.loads(str(await bot.get_stranger_info(user_id=int(i), no_cache=False)).replace('\'', '"').replace('\\','\\\\'))['nickname']
        e += f'\n{n+1} -  {g}    ({j})'
    await baihang.finish(e)

chakan = on_command('查看资产')


@chakan.handle()
async def _(event: GroupMessageEvent):
    uid = str(event.user_id)
    with open(f'{current_path}score.json', 'r') as a:
        d = json.loads(a.read())
    with open(f'{current_path}things.json','r') as b:
        c=json.loads(b.read())
        try:
            sc = d[uid]
        except KeyError:
            await chakan.finish(Message(f'[CQ:at,qq={uid}]\n你还没有签到过'))
        try:
            th=c[uid]
        except KeyError:
            await chakan.finish(Message(f'[CQ:at,qq={uid}]\n你现在有 {sc} 积分'))
        msg = f'[CQ:at,qq={uid}]\n你现在有 {sc} 积分'
        for i,j in zip(th.keys(),th.values()):
            msg+=f'\n{i} {j} 个'
        await chakan.finish(Message(msg))
        '''
        match sc:
                case 20:
                    msg = f'你现在有 {sc} 积分'
                case 100:
                    msg = f'你现在有 {sc} 积分！'
                case 500:
                    msg = f'你现在有 {sc} 积分！！！'
            await chakan.finish(msg)
        except KeyError:
            await chakan.finish('你还没有签到过诶')
            '''

things={'亲亲':10}
store=on_command('积分商店')
@store.handle()
async def _():
    msg='        Sut - 商店'
    names=list(things.keys())
    for i in names:
        msg+=f'\n    {i}(发送"亲@demo"，Sut将会禁言demo三分钟)\n    价格: {things[i]}积分'
    msg+='\n发送"购买demon个"，将会自动扣除积分购买n个demo'
    await store.finish(msg)

goumai=on_command('购买')
@goumai.handle()
async def _(event:GroupMessageEvent):
    gmg=event.get_plaintext()
    uid=event.get_user_id()
    res=findall('购买(.*)',gmg)[0]
    nm=int(findall('(\d*)个',res)[0])
    th=res.replace(f'{nm}个','')
    if th in things.keys():
        with open(f'{current_path}score.json', 'r') as a:
            ddd=json.loads(a.read())
            if ddd[uid]<things[th]*nm:
                await goumai.finish(Message(f'[CQ:at,qq={uid}]你只有{ddd[uid]}积分，无法兑换此物品'))
            else:
                ddd[uid]-=things[th]*nm
                with open(f'{current_path}things.json','r') as b:
                    dic=json.loads(b.read())
                    try:
                        dic[uid][th]+=nm
                    except KeyError:
                        dic[uid]={}
                        dic[uid][th]=nm
                    finally:
                        with open(f'{current_path}things.json','w') as c:
                            c.write(json.dumps(dic))
                        with open(f'{current_path}score.json','w') as c:
                            c.write(json.dumps(ddd))
                        await goumai.finish(Message(f'[CQ:at,qq={uid}]购买成功！'))
    else:
        await goumai.finish('暂时还没有此物品，可以向开发人员申请添加')


qin=on_command('亲')
@qin.handle()
async def _(event:GroupMessageEvent,bot:Bot):
    uid=event.get_user_id()
    gid=event.group_id
    at=findall('qq=(.*?)\]',str(event.get_message()))[0]
    with open(f'{current_path}things.json','r') as a:
        dic=json.loads(a.read())
        try:
            if dic[uid]['亲亲']<1:
                await qin.finish(Message(f'[CQ:at,qq={uid}]\n你的亲亲不足，请前往商店购买'))
        except KeyError:
            await qin.finish(Message(f'[CQ:at,qq={uid}]\n你的亲亲不足，请前往商店购买'))
    try:
        await bot.set_group_ban(group_id=gid,user_id=int(at),duration=180)
        with open(f'{current_path}things.json','w') as b:
            dic[uid]["亲亲"]-=1
            b.write(json.dumps(dic))
            g = json.loads(str(await bot.get_stranger_info(user_id=at, no_cache=False)).replace('\'', '"'))['nickname']
            await qin.finish(Message(f'[CQ:at,qq={uid}]亲了[CQ:at,qq={at}]一口\n{g} 暂时无法说话。'))
    except ActionFailed:
        await qin.send('亲亲失败')
    finally:
        await qin.finish()



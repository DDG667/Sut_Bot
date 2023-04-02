from re import findall
from base64 import b64encode
from hashlib import md5
from json import loads
from requests import get
from random import choice, randint
from nonebot.matcher import Matcher
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import ActionFailed, Bot, Message, GroupMessageEvent
from nonebot.adapters.cqhttp import MessageSegment
from ..func import send

'''
cheng=on_command('')
@cheng.handle()
async def _():
    pass

@cheng.receive()
async def _(event=GroupMessageEvent):
    msg=event.get_plaintext()
    findall()(f'https://www.cyjl123.com/p/{msg}').text'''
async def c(m):
    msg = loads(
        get('http://api.qingyunke.com/api.php?key=free&appid=0&msg='+m).text)['content']
    if '{face' in msg:
        a = msg.split('}')[0]
        a = a.split(':')[-1]
        msg = f'[CQ:face,id={a}]'+msg.split('}')[-1]
    if '菲菲' in msg:
        msg = msg.replace('菲菲', 'ATRI')
    if '周超辉' in msg:
        msg = msg.replace('周超辉', 'DDG667')
    if '595577505' in msg:
        msg = msg.replace('595577505', '3580426231')
    if '1938877131' in msg:
        msg = msg.replace('1938877131', '3580426231')
    if '日本人' in msg or '未获取到相关信息'in msg or '签到' in msg or '梅州' in msg or '儿子' in msg:
        await chat.finish()
    return msg.replace('　','').replace('{br}','\n')

chat = on_command('',priority=50)

def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

async def translate(word,a='zh',b='en'):
    aid='20221028001423168'
    rint=randint(1000000000,1999999999)
    key='GOeTz0p_QXrkfief2t3y'
    sign=md5(f'{aid}{word}{rint}{key}'.encode()).hexdigest()
    r=get(f'https://fanyi-api.baidu.com/api/trans/vip/translate?q={word}&from={b}&to={a}&appid={aid}&salt={rint}&sign={sign}').text
    try:
        w=loads(r)["trans_result"][0]["dst"]
    except KeyError:
        w=word
    finally:
        return w
@chat.handle()
async def chat_handle(bot:Bot,event: GroupMessageEvent, args: Message = CommandArg()):
    if loads(get(f'https://api.wer.plus/api/min?t={args.extract_plain_text()}').text)['num']>0 and (event.group_id==551099482) or '你妈' in args.extract_plain_text():
        try:
            await bot.delete_msg(message_id=event.message_id)
            await bot.set_group_ban(group_id=event.group_id,user_id=event.user_id,duration=180)
            await chat.finish(Message(f'[CQ:at,qq={event.user_id}]消息中包含违禁词，禁言3分钟!'))
        except ActionFailed as af:
            print(af)
            await chat.finish()
    '''
    if event.group_id==686221881:
            await bot.send_group_msg(group_id=179264018,message=Message(f'{event.sender.nickname}：')+event.message)
    '''
    if 686221880!=686221881:
        if event.group_id==582489481:
            await chat.finish(event.json())
        elif event.dict()['to_me']:
            if '爱' in args.extract_plain_text():
                await chat.finish()
            pass
        else:
            await chat.finish()
    if ('http:' or 'https:' or '.org' or 'www.' or '.cn' or '.com' or '.xyz' or '.onion') in args.extract_plain_text():
       # if requests.get(findall('(http.*)',args.extract_plain_text())[0]).status_code==200:
        await bot.delete_msg(message_id=event.message_id)
        await bot.set_group_ban(group_id=event.group_id,user_id=event.user_id,duration=180)
        await chat.finish('禁止发送链接！禁言3分钟')
    if '老婆' in args.extract_plain_text():
        if event.user_id != 3580426231:
            await chat.finish('注意称呼')
    if len(args.extract_plain_text())>256:
        await bot.delete_msg(message_id=event.message_id)
        await chat.finish()
    if is_contain_chinese(args.extract_plain_text()) or 'help' in args.extract_plain_text():
        a=args.extract_plain_text()
        b=True
    else:
        a=await translate(args.extract_plain_text())
        b=False
    a=a.replace('叫','').replace('ATRI','莉莉')
    w=await c(a)
    if not b:
        w=await translate(w,a='en',b='zh')
    await chat.finish(Message(w))
   # xml=f'''<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="35" templateID="1" action="viewMultiMsg" brief="[QQ红包]恭喜发财" m_resid="ja6YTKhcYYYA77DKMi0fMgVQlQcsXDjhCxmDwHtlhnJAi31GV2PDQNqDmg7Lyix7" m_fileName="7183291257405535308" tSum="1" sourceMsgId="0" url="" flag="3" adverSign="0" multiMsgFlag="0"><item layout="1" advertiser_id="0" aid="0"><title size="26" color="#777777" maxLines="2" lineSpace="12">{w}</title></item><source name="[QQ红包]恭喜发财" icon="" action="" appid="-1" /></msg>'''
   # await chat.finish(MessageSegment.xml(xml))

# chatp=on_command('',rule=PrivateMessageEvent)
# @chatp.handle()
# async def ccc( PrivateMessageEvent,):
#    await c(args.extract_plain_text())
tiangou = on_command('舔狗')


@tiangou.handle()
async def gou():
    msg = get('https://api.oick.cn/dog/api.php').text
    await tiangou.finish('舔狗日记:\n'+msg)

yulu = on_command('语录')


@yulu.handle()
async def yu():
    msg = get(' https://api.oick.cn/yulu/api.php').text
    await yulu.finish(msg)

dutang = on_command('毒汤')


@dutang.handle()
async def du():
    msg = get('https://api.oick.cn/dutang/api.php').text
    await dutang.finish(msg)

ips = on_command('IP')


@ips.handle()
async def cha(event: GroupMessageEvent):
    ip = event.get_plaintext().split(' ')[-1]
    info = loads(get(f'http://ip-api.com/json/{ip}?lang=zh-CN').text)
    if info["status"] == 'success':
        await ips.send('查询成功，不愧是高性能的我')
        await ips.finish(f'国家名称:{info["country"]}\n国家代号:{info["countryCode"]}\n城市:{info["city"]}\n时区:{info["timezone"]}\n纬度:{info["lat"]}  经度:{info["lon"]}')
    elif info['status'] == 'fail':
        await ips.finish(Message('查询失败[CQ:face,id=106]'))

tou = on_command('头像')


@tou.handle()
async def touc(event: GroupMessageEvent):
    sex = str(event.message).split(' ')[-1]
    img = get(loads(get(
        f'https://api.uomg.com/api/rand.avatar?sort={sex}&format=json').text)['imgurl']).content
    await tou.finish(MessageSegment.image(img))

tu = on_command('土味情话', block=False)


@tu.handle()
async def tuw():
    msg = get('https://api.uomg.com/api/rand.qinghua?format=text').text
    await tu.finish(msg)

sh = on_command('短网址')


@sh.handle()
async def sho(event: GroupMessageEvent):
    url = str(event.message).split(' ')[1]
    json = loads(
        get(f'https://api.uomg.com/api/long2dwz?dwzapi=tcn&url={url}').text)
    await sh.finish(json['ae_url'])

qr = on_command('qr', aliases={'QR'})


@qr.handle()
async def qrc(event: GroupMessageEvent):
    url = str(event.message).split(' ')[-1]
    qrco = get(f'https://api.oick.cn/qrcode/api.php?text={url}&size=4096').content
    await qr.finish(MessageSegment.image(qrco))

weat = on_command('天气')


@weat.handle()
async def wea(event: GroupMessageEvent):
    area = event.get_plaintext().split(' ')[-1]
    url = f'https://api.66mz8.com/api/weather.php?location={area}'
    da = loads(get(url,verify=False).text)
    if da['code'] == 200:
        data1 = f'          {area}天气'
        for data in da['data']:
            data1 += f"\n{data['days']}    {data['week']}\n{data['temperature']}  {data['weather']}  {data['wind']}"
        await weat.send(data1)
        await weat.finish()
    else:
        await weat.finish('请告诉ATRI你要查哪个地区的天气，OK?')

hitokoto_matcher = on_command("一言")


@hitokoto_matcher.handle()
async def hitokoto(matcher: Matcher, ):
    a = [True, False]
    if choice(a):
        m = loads(get("https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=h").text)
        if m['from_who'] != None:
            msg = f"{m['hitokoto']}\n——《{m['from']}》{m['from_who']}"
        else:
            msg = f"{m['hitokoto']}\n——《{m['from']}》"

    else:
        msg = get('https://api.oick.cn/yiyan/api.php').text
    await matcher.finish(msg)

yiju = on_command("一句")


@yiju.handle()
async def yiju_handle():
    await yiju.finish(get('http://api.yanxi520.cn/api/xljtwr.php?charset=utf-8http://api.yanxi520.cn/api/xljtwr.php?encode=txt').text)

dongman = on_command('动漫图')


@dongman.handle()
async def _():
    json = loads(
        get('https://www.yuanxiapi.cn/api/img/?type=dongman&format=json').text)
    if json['code'] == 200:
        data = get(json['imgurl']).content
        await dongman.finish(MessageSegment.image(data))
    else:
        await dongman.finish(Message('Get到了但状态码不是200，ATRI无能为力[CQ:face,id=106]'))


yiwen = on_command('一文')


@yiwen.handle()
async def _():
    with get('https://meiriyiwen.com/') as a:
        t = findall('<h1>(.*)</h1>', a.text)[0]
        w = findall(
            '<p class="article_author"><span>(.*)</span></p>', a.text)[0]
        cl = findall('<p>(.*)</p>', a.text)
        c = ''
        for i in cl:
            c += '\n'*2+' '*4+i
        c = ' '*6+t+'\n'+' '*8+w+c
        await send(yiwen,c)
        await yiwen.finish()

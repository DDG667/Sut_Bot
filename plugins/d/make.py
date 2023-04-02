from pickle import dump, load
from classes import user, users
from json import loads
from asyncio import run


"""
us = users([])


async def create_user(id):
    with open("./score.json", "r") as sco:
        score = loads(sco.read())
        with open("./things.json") as thi:
            thing = loads(thi.read())
            u = user(id)
            await u.aset_score(score[str(id)])
            await u.achange_score(thing.get(str(id), {"亲亲": 0})["亲亲"] * 10)
            global us
            us.add_users([u])


async def start():
    with open("./score.json", "r") as a:
        for i in list(loads(a.read()).keys()):
            await create_user(i)
    print(await us.aget_scores_list())


run(start())
with open("./pydata", "wb") as pydata:
    dump(us, pydata)
"""
# with open("./pydata", "rb") as a:
#     us: users = load(a)
# print(us)
"""
with open("./things.json", "r") as a:
    d = loads(a.read())
    print(d)
    for i in d:
        try:
            users[i].change_thing(kiss, d[str(i)]["亲亲"])
        except KeyError:
            continue
"""
# print(load(a)["2387665291"])
# print(load(a)["2387665291"].get_score())
async def get():
    a = open("./pydata", "rb")
    print(await load(a)["3580426231"].aget_score())
    a = open("./pydata", "rb")
    print(await load(a)["3580426231"].aget_score())


# run(get())


import pickle

a:list[user]=[]












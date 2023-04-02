from classes import user, users
from json import loads
from pickle import dump, load

"""
us = users([])
sco: dict = loads(open("./score.json", "r").read())
thi: dict = loads(open("./things.json", "r").read())
for j, i in enumerate(sco, start=0):
    u = user(int(i))
    u.aset_score(sco[i])
    try:
        u.achange_score(thi[i]["亲亲"] * 10)
    except KeyError as e:
        print(e)
    us.add_user([u])

# print(us[3580426231].aget_score())
with open("./pydata", "wb") as data:
    dump(us, data)
"""

with open("./pydata", "rb") as data:
    us = load(data)
    print(us[3580426231].aget_score())

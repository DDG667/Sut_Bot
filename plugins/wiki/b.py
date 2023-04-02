from a import a
from os import listdir
from requests import get

e = listdir("./linuxc/")
it = 0
for i in a:
    with get(i) as b:
        i = i.split("/")[-1].split(".")[0]
        if i in e:
            continue
        with open("linuxc/" + i, "wb") as c:
            c.write(b.content)
            print(it + 1, i, end="    ")
        b.close()

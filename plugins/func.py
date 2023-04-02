async def send(ma, string: str):
    if len(string) > 1024:
        await ma.send(string[0:1024])
        await send(ma, string[1024:])
    else:
        await ma.send(string)

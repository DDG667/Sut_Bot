from PIL import Image, ImageDraw,ImageFont
import os
current_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".") + "/"
def draw(txt:str):
    im = Image.open(f"{current_path}img.jpg")
    img = ImageDraw.Draw(im)
    font=ImageFont.truetype(f"{current_path}font.ttf",200)
    if len(txt)<8:
        img.text((200,1200), txt,font=font, fill=(0, 0, 0))
    elif len(txt)<14:
        img.text((200, 1100), txt[0:8],font=font, fill=(0, 0, 0))
        img.text((200,1300),txt[8:],font=font,fill=(0,0,0))
    elif len(txt)<57:
        font=ImageFont.truetype(f"{current_path}font.ttf",120)
        img.text((200,1100),txt[0:13],font=font,fill=(0,0,0))
        img.text((200,1220),txt[13:27],font=font,fill=(0,0,0))
        img.text((200,1340),txt[27:41],font=font,fill=(0,0,0))
        img.text((200,1460),txt[41:],font=font,fill=(0,0,0))
    else:
        return open(f'{current_path}im.jpg','rb').read()
    im.save(f"{current_path}imt.jpg")
    return open(f'{current_path}imt.jpg','rb').read()

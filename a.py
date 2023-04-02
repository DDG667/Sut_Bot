from qrcode import QRCode
import io

qrcode = QRCode(version=1, box_size=200)
qrcode.add_data("http://github.com/DDG667")
img = qrcode.make_image()
a = io.BytesIO()
img.save(stream=a)
a.seek(0)
open("./a.png", "wb").write(a.read())

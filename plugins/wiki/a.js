pip install wheel
pkg install libjpeg-turbo -y
LDFLAGS="-L/system/lib64/" CFLAGS="-I/data/data/com.termux/files/usr/include/" pip install Pillow --no-cache-dir
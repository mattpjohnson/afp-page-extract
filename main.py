'''
Extracts a specified page from an AFP file

Usage:
    extract.py input.afp output.afp pageno

'''
import sys
import codecs
import struct
import binascii

def getLength(header):
    length = 0
    for i in range(1, len(header)):
        length = (length<<8) | ord(header[i])
    return length

ifile = open(sys.argv[1], 'rb')
ofile = open(sys.argv[2], 'wb')
pageno = int(sys.argv[1])

header = ifile.read(3)
pages = 0
inpage = False
page = ''

while True:
    length = getLength(header)
    text = ifile.read(length-2)
    type = text[:3]

    if type == chr(0xd3)+chr(0xa8)+chr(0xaf):
        pages += 1
        inpage = True
    elif type == chr(0xd3)+chr(0xa9)+chr(0xaf):
        inpage = False
        if pages == pageno:
            ofile.write(page)
        page = ''

    text = header+text

    if inpage:
        page += text
    else:
        ofile.write(text)

    header = ifile.read(3)

    if not header:
        # EOF
        break

    assert ord(header[0]) == 90

ifile.close()
ofile.close()

print pages
#!/usr/bin/env python3

from PIL import Image
import argparse


def hideInFile(args):
    inim = Image.open(args.infile)
    hideim = Image.open(args.hidefile)
    assert inim.size == hideim.size, "Both image must be of the same size"
    bits = args.bits
    assert 0 <= bits <= 8
    outim = Image.new('RGB', inim.size)
    for x in range(inim.size[0]):
        for y in range(inim.size[1]):
            incol = inim.getpixel((x, y))
            hidecol = hideim.getpixel((x, y))
            outcol = []
            for cp in range(len(incol)):
                inbyt = '{0:08b}'.format(incol[cp])
                hidebyt = '{0:08b}'.format(hidecol[cp])
                outbyt = inbyt[:8 - bits] + hidebyt[bits - 1::-1]
                outcol.append(int(outbyt, 2))
            outim.putpixel((x, y), tuple(outcol))
    inim.close()
    hideim.close()
    outim.save(args.outfile, 'PNG')
    outim.close()


def inverseFile(args):
    inim = Image.open(args.infile)
    outim = Image.new('RGB', inim.size)
    xS, yS = inim.size[0], inim.size[1]
    for x in range(xS):
        for y in range(yS):
            pos = (x, y)
            incol = inim.getpixel(pos)
            outcol = []
            for cp in range(len(incol)):
                inbyt = '{0:08b}'.format(incol[cp])
                outbyt = inbyt[::-1]
                outcol.append(int(outbyt, 2))
            outim.putpixel(pos, tuple(outcol))
    inim.close()
    outim.save(args.outfile, 'PNG')
    outim.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Hide an image inside another and decode images")

    parser.add_argument('infile', metavar='INFILE', type=str, help="Input file")

    subparsers = parser.add_subparsers(dest='action')
    subparsers.required = True

    hidep = subparsers.add_parser('hide')
    hidep.add_argument('hidefile', metavar='HIDEFILE', type=str, help="File to hide")
    hidep.add_argument('bits', metavar='BITS', type=int, help="Number of bits to use for hiding")
    hidep.set_defaults(func=hideInFile)

    inversep = subparsers.add_parser('inverse')
    inversep.set_defaults(func=inverseFile)

    parser.add_argument('outfile', metavar='OUTFILE', type=str, help="Output file")

    args = parser.parse_args()
    args.func(args)

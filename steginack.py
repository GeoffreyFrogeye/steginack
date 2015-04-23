#!/usr/bin/env python3

from PIL import Image
import argparse
from eta import ETA

get_bin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)
# From http://stackoverflow.com/a/21732313/2766106


def hideInFile(args):
    inim = Image.open(args.infile)
    hideim = Image.open(args.hidefile)
    assert inim.size == hideim.size, "Both image must be of the same size"
    assert 0 <= args.bits <= 8
    outim = Image.new('RGB', inim.size)
    eta = ETA(inim.size[0] * inim.size[1])
    for x in range(inim.size[0]):
        for y in range(inim.size[1]):
            incol = inim.getpixel((x, y))
            hidecol = hideim.getpixel((x, y))
            outcol = []
            for cp in range(len(incol)):
                inbyt = get_bin(incol[cp], 8)
                hidebyt = get_bin(hidecol[cp], 8)
                outbyt = list(inbyt)
                for bit in range(args.bits):
                    outbyt[-bit - 1] = hidebyt[bit]
                outcol.append(int(''.join(outbyt), 2))
            outim.putpixel((x, y), tuple(outcol))
            eta.print_status(x * inim.size[1] + y)
    eta.done()
    inim.close()
    hideim.close()
    outim.save(args.outfile, 'PNG')


def inverseFile(args):
    inim = Image.open(args.infile)
    outim = Image.new('RGB', inim.size)
    eta = ETA(inim.size[0] * inim.size[1])
    for x in range(inim.size[0]):
        for y in range(inim.size[1]):
            incol = inim.getpixel((x, y))
            outcol = []
            for cp in range(len(incol)):
                inbyt = get_bin(incol[cp], 8)
                outbyt = list(inbyt)
                for bit in range(8):
                    outbyt[-bit - 1] = inbyt[bit]
                outcol.append(int(''.join(outbyt), 2))
            outim.putpixel((x, y), tuple(outcol))
            eta.print_status(x * inim.size[1] + y)
    eta.done()
    inim.close()
    outim.save(args.outfile, 'PNG')


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

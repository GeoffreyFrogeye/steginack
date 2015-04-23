#!/usr/bin/env python3

from PIL import Image
import argparse


def hideInFile(infile, hidefile, bits, outfile):
    inim = Image.open(infile)
    hideim = Image.open(hidefile)
    assert inim.size == hideim.size, "Both image must be of the same size"
    outim = Image.new('RGB', inim.size)
    inim.close()
    hideim.close()
    outim.save(outfile, 'PNG')

def inverseFile(infile, bits, outfile):
    inim = Image.open(infile)
    outim = Image.new('RGB', inim.size)
    inim.close()
    outim.save(outfile, 'PNG')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Hide an image inside another and decode images")
    parser.add_argument('infile', metavar='INFILE', type=str, help="Input file")
    parser.add_argument('bits', metavar='BITS', type=int, help="Number of bits to use")
    parser.add_argument('outfile', metavar='OUTFILE', type=str, help="Output file")
    parser.add_argument('-s', '--hide', type=str, help="File to hide")
    args = parser.parse_args()
    if args.hide:
        hideInFile(args.infile, args.hide, args.bits, args.outfile)
    else:
        inverseFile(args.infile, args.bits, args.outfile)

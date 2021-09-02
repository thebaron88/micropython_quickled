import argparse
from littlefs import LittleFS
import os

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--dir', dest='folders', action='append', required=True, help='list of dirs that we want to add to the folder')
parser.add_argument('--out', dest='outfile', action='store', required=True, help='output file for the image')
parser.add_argument('--block_size', dest='block_size', action='store', type=int, default=4096, help='LittleFS block size')
parser.add_argument('--block_count', dest='block_count', action='store', type=int, default=240, help='LittleFS block count')

args = parser.parse_args()

fs = LittleFS(block_size=args.block_size, block_count=args.block_count)

for folder in args.folders:
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            with fs.open(name, 'w') as fh:
                fh.write(open(path,"rb").read())

with open(args.outfile, 'wb') as fh:
    fh.write(fs.context.buffer)

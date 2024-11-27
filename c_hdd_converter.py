import os.path
import pickle
import os

from tqdm import tqdm

import argparse

parser = argparse.ArgumentParser(
                    prog='Bin to c_hdd',
                    description='Converts a binary file to a c_hdd image')

parser.add_argument('input',help="Binary File to convert")           # positional argument
parser.add_argument('output',help="c_hdd File to output") 
parser.add_argument('-m', '--max_size',default=0x32000,help="Sets the max LBA of the disk image, defaults to 0x32000 which is 100MB, if your binary is larger, the LBA will expand to fit it.")      # option that takes a value


args = parser.parse_args()


if not os.path.isfile(args.input):
    print(args.input, "Does not exist!")
    exit(-1)

max_size = 0
try:
    max_size = int(args.max_size)
except:
    try:
        max_size = int(args.max_size,16)
    except:
        print(args.max_size,"Is not a valid integer OR HEX number")


if max_size > 0x400000:
    print("This converter only supports outputting a 2GB c_hdd image. A max size of ",max_size," would make a ",(max_size*512)/1024/1024/1024,"GB file")
    exit(-1)


print("Converting",args.input,"with at least",hex(max_size),"sectors and writing it to",args.output)

data_input = open(args.input,"rb")
output = open(args.output,"wb+")



input_size = os.stat(args.input).st_size

output_size = (input_size//512) + (input_size%512 != 0)

max_size = max(output_size,max_size)

drive = {"max_lba":max_size}


print("writing file to image")
for x in tqdm(range(output_size)):
    drive[x] = data_input.read(512)
last_lba = x

print("padding end of file sector")
if len(drive[last_lba]) < 512:
    for x in tqdm(range(512 - len(drive[last_lba]))):
        drive[last_lba] += b"\00"

pickle.dump(drive,output)

data_input.close()
output.close()

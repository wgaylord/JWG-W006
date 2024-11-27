import json
import os.path
import os

from tqdm import tqdm

import argparse

parser = argparse.ArgumentParser(
                    prog='IR Builder',
                    description='Builds IR to ASM')

parser.add_argument('input',help="IR in")           # positional argument
parser.add_argument('output',help="asm out") 


args = parser.parse_args()

if not os.path.isfile(args.input):
    print(args.input, "Does not exist!")
    exit(-1)
    
program = json.load(open(args.input))

types = program["types"]
program = program["program"]


globalVars = {}

for x in program:
    op = x[0]
    
    if op == "globalInfo":
        globalVars = x[1]
    

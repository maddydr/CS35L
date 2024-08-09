#!/usr/bin/env python3.11
import random
import sys
import argparse
from argparse import ArgumentParser

class shuf:
    def __init__(self, input): # initializes shuf object with input and numLine
        self.lines = input # making an attribute called lines
        self.linecount = len(self.lines)
    def randomlines(self): # input self knows its talking about its own class
        return random.choice(self.lines) # function of shuf class that returns a random line
    def randomsample(self, count=None):
        if count and count < self.linecount: return "".join(random.sample(self.lines, count))
        else: return "".join(random.sample(self.lines, self.linecount))
        # if a count is specified and count is less than the total lines of input, then use those specified lines, else use all lines

def main():
    usage_msg = """./shuf.py [OPTION] ... FILE
    or: ./shuf.py -e [OPTION] ... [ARG]...
    or: ./shuf.py -i LO-HI [OPTION]...

    DESCRIPTION
    Write a random permutation of the input lines to standard output.

    With no FILE, or when FILE is -, read standard input.

    Mandatory arguments to long options are mandatory for short options too."""
    
    parser = ArgumentParser(usage=usage_msg)
    parser.add_argument('file', type=argparse.FileType("r"), nargs='?') # type must be a readable file
    # creates parser object and gives usage message
    # adds optional arguments
    parser.add_argument('-e', '--echo', help='treat each ARG as an input line', nargs='*')
    # adding the echo command, it can accept 0 or more values for command line (*)
    parser.add_argument('-i', '--input-range', help='treat each number LO though HI as an input line')
#    parser.add_argument('filename',nargs='?') # !! DONT UNDERSTAND WHY WE ADD THIS HERE? HOW DOES IT EFFECT THE FOLLOWING ARGUMENTS? DONT GET THE PURPOSE OF ADDING 'FILE' NAME TYPE ARGUMENTS
    parser.add_argument('-n', '--head-count', help='output at most COUNT lines', type=int)
    parser.add_argument('-r','--repeat', help='output lines can be repeated', action='store_true')

    args = parser.parse_args();  # creates namespace object with all the arguments we added to it 'file', '-head_count, -repeat, etc'
    totalLines = args.head_count # only will have a value if -n is used
    inputLines = []

    try:
        args, unk = parser.parse_known_args()
    except Exception as e:
        exit(1)
    # parse the args, put them in args and unk variable, if an exception is raised, exit
    if args.file:
        if args.input_range or args.echo:
            parser_error("Extra operand")
        try:
            inputLines = args.file.readlines()
        except:
            parser.error("I/O error")
    elif args.input_range:
        lo, hi = map(int, args.input_range.split("-")) # assigns lo and hi integers from input
        numberRange = list(range(lo, hi+1))
        for e in numberRange:
            inputLines.append(str(e) + '\n')
            
       # numberRange = (str(e) for e in numberRange)
       # inputLines = [num + '\n' for num in numberRange]
    elif args.echo:
        echoArg = args.echo
        inputLines = [string + '\n' for string in echoArg] # rewrite in for loop form
    else:
        try: 
            args.file = sys.stdin # no file so it will be standard input
            inputLines = args.file.readlines()
        except: 
            parser.error("I/O error")

    shuffler  = shuf(inputLines)
    
    if args.repeat is True:
       if totalLines: 
           for x in range(totalLines):
               sys.stdout.write(shuffler.randomlines())
       else: 
           while not totalLines: 
               try:
                   sys.stdout.write(shuffler.randomlines())
               except:
                   exit(1)
    else:
       sys.stdout.write(shuffler.randomsample(totalLines))


       
if __name__ == "__main__":
    main()

#!/usr/bin/env python3

# Example help menu python3 insertfinder.py -h
# Example run: python3 insertfinder.py GA[TC]CA[GA]GC[ACGT]AC[ACGT] test.txt testoutput.txt
# python3 regexinsertfinder.py GA[TC]CA[GA]AA[TC]GC[ACGT]AC[ACGT] RNaseAcollapse.fasta output_regex_RNAseA.txt

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('matchstring', help='string to match')
parser.add_argument('filelocation', help='file to scan')
parser.add_argument('outputfilelocation', help='file to output to')
parser.add_argument('--startfromsequence', type=int, default=1, help='optional line number to start from')
args = parser.parse_args()

#Prepare .csv compatible text output file
outputfile = open(args.outputfilelocation, "a+")
outputfile.write("%s,%s,%s,%s\n" % ("Sequence", "SeqLen", "ReadCount", "MatchCount"))

f = open(args.filelocation, "r")
lines = f.readlines()

# Start FASTA input text file count lines at 1
curr_sequence = 1
curr_frequency = ""

for line in lines:
    if line.startswith(">"):
        curr_sequence += 1
        seq = 0
        try:
            hyphen_pos = line.find("-")
            endlength = len(line)
            seqstr = line[1:hyphen_pos]
            frequency = line[hyphen_pos + 1:-1]
            seq = int(seqstr)
        except:
            print("ERROR: parsing line: " + line)
            seq = 0
            frequency = "null"
        curr_sequence = seq
        curr_frequency = frequency
        continue
    if args.startfromsequence > 1 and curr_sequence < args.startfromsequence:
        continue
    
    matches = 0
    match_indexes = []
    matchpos = 0
    
    while True:
        #Search line for pattern
        pattern = re.compile(args.matchstring)
        patternMatch = pattern.search(line, matchpos)
        curr_len = len(line)
        # patternMatch will be None if there is no match
        if patternMatch == None:
            break
        else:
            #Add the location and pattern for each match
            matchpos = patternMatch.start()
            match_indexes.append(str(matchpos + 1))
            match_indexes.append(patternMatch.group())
            matchpos += 1
            matches += 1
    #Append information for each sequence
    newRow = "%d,%d,%s,%d" %(curr_sequence, curr_len, curr_frequency, matches)
    #Append match location and pattern if exists
    if matches > 0:
        newRow = newRow + "," + ",".join(match_indexes) + "\n"
    else:
        newRow = newRow + "\n"
        
    outputfile.write(newRow)
    print(newRow)
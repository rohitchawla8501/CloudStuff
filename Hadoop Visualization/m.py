#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    #words = line.split("\t")
    # increase counters
     x = int(line[2][:4])
     t = int(line[3])
	print '%s\t%s' % (x,t)
    '''for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
		print '%s\t%s' % (word[1], 1)'''
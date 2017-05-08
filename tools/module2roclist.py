#!/usr/bin/env python
import fileinput

# read from either command line argument or stdin
for line in fileinput.input():
    if '_LYR1_' in line:
        rocs = [0, 1, 2, 3, 12, 13, 14, 15] if 'F_MOD' in line else [4, 5, 6, 7, 8, 9, 10, 11]
    else:
        rocs = range(0, 16)
    lineParts = line.strip('\n').split(' ')
    for i in rocs:
        if len(lineParts) > 1 and line.startswith('BPix'):
            print lineParts[0] + '_ROC%d'%i + ' ' + ' '.join(lineParts[1:])
        else:
            print line
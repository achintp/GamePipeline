import sys
import json
import pprint

def JsonToText(fname, outname):
	with open(fname, 'r') as jFile:
		data = json.load(jFile)

	with open(outname, 'w') as outFile:
		pprint.pprint(data, outFile)

if __name__=='__main__':
	JsonToText(sys.argv[1], sys.argv[2])
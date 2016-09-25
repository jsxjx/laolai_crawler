# -*- coding: utf-8 -*-
from laolai_crawl_util import *
import sys, getopt

def main(argv):

	if len(argv) != 2:
		print 'python run_laolai_crawler.py  -i <nameInputFile> '
	inputfile = str(argv[1])
	words = open(inputfile,'r').readlines()
	for w in words:
		w = w.strip()

		username = w
		output_path = "result/laolai_info_"+username+".json"
		output = open(output_path, "w")
		crawler_exe(username,output)

		output.close()

		print "crawling complete"

if __name__ == '__main__':
    main(sys.argv[1:])
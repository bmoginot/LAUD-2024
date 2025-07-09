# gets the first 10k reads of each fastq file for a given list of participant numbers

import sys
import argparse
import glob
import os

def get_args(args):
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--participants", # take list of participants to subset
						nargs="+",
						help="<Required> Set flag",
						required=True)
	return parser.parse_args(args)

def subset(path, datadir):
	patnum = os.path.split(path)[1]
	patdir = os.path.join(datadir, patnum)

	if os.path.isdir(patdir):
		os.system(f"rm -r {patdir}")
	os.mkdir(patdir)

	for fastq_file in glob.glob(f"{path}/*.fastq.gz"):
		filename = os.path.split(fastq_file)[1]
		filename = filename.replace(".fastq.gz", "-subset.fq")
		outfile = os.path.join(patdir, filename)
		os.system(f"zless {fastq_file} | head -n 40000 > {outfile}")

def main():
	args = get_args(sys.argv[1:])

	reads = glob.glob("/media/catherine/Seagate/EEK/*")
	
	datadir = "data/subset/"
	if not os.path.isdir(datadir):
		os.mkdir(datadir)

	for path in reads:
		if os.path.split(path)[1][3:] in args.participants: # get directories of all participants entered in command line
			subset(path, datadir)

if __name__ == "__main__":
	main()

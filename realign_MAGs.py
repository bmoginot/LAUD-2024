# align reads for given participant(s) against a bladder mag and assemble reads that write out

import os
import sys
import glob
import argparse
import pandas as pd
import time
import subprocess

def get_args(args):
	"""retrieve command line arguements"""
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--participants", nargs="+", required=True) # get list of participants to align and assemble
	parser.add_argument("-t", "--threads")
	return parser.parse_args(args)

def get_bladder_samples():
	"""extract only bladder samples from the eek spreadsheet so that they can be filtered out from the reads"""
	header = ["sample", "study", "ecoli_pos", "timepoint", "date", "type", "method", "body_site", "filename"]
	eek = pd.read_excel("EEK Samples.xlsx", names=header)
	just_bladder_sites = eek["body_site"].map(lambda x: x.lower())==("bladder") # get only entries where the sample was collected from the bladder
	just_bladder_samples = eek[just_bladder_sites]["sample"].map(str) # get all samples that came from the bladder only
	return list(just_bladder_samples)

def filter_reads(reads, bladder_samples):
	"""filter out bladder reads since we're aligning to the bladder MAG"""
	non_bladder_samples = []
	for r in reads:
		if any([sam in r for sam in bladder_samples]): # if the sample number of any bladder samples is found in the read path, it is ignored
			pass
		else:
			non_bladder_samples.append(r)
	return non_bladder_samples

def build_index(mag, ind):
	"""build index from mag for bowtie alignment"""
	print("building index...")
	
	subprocess.run([ # build index to act as reference for bt2
		"bowtie2-build", "-q", mag, ind
	])

	print(f"done\n")

	return

def run_bowtie(ind, reads, threads, out, log):
	"""run bowtie, aligning each non-bladder read to the bladder mag using --very-fast heuristic"""
	proc = str(threads) if threads else "1"
	
	print(reads)

	for i in range(0, len(reads), 2):
		fread = reads[i]
		rread = reads[i+1]
		sample_num = fread.split("_")[0]
		print(sample_num + "...", end=" ")

		result = subprocess.run([
			"bowtie2",
			"--very-fast",
			"-p", proc,
			"-x", ind,
			"-1", fread,
			"-2", rread,
			"-S", os.path.join(out, sample_num + "_map.sam"),
			"--al-conc", os.path.join(out, sample_nam + "_%.fq")
			],
			capture_output = True,
			text = True
		)

		log.write(f"{sample_num}:\n")

		for line in result.stderr.splitlines(): # write out percent alignment rate for each parameter
			if "overall alignment rate" in line:
				log.write(f"{line}\n\n")

		with open("errors.log", "w") as e:
			e.write(result.stdout)

	print()

	return


def main():
	start = time.time() # how long does this take to run

	args = get_args(sys.argv[1:])

	outdir = os.path.abspath("output")
	if os.path.isdir(outdir):
		os.system(f"rm -r {outdir}")
	os.mkdir(outdir)

	subset_reads = "/data/subset/" # path to subset reads we are using for testing # eek_data = "/media/catherine/Seagate/EEK/" # path to EEK directory, which contains all participant reads
	mags_path = "/media/catherine/Seagate/HPCC_Backup/aavalos4/making_mags/MAGS/" # path to Lexi's dir with the mags

	bladder_samples = get_bladder_samples()

	log = open(os.path.join(outdir, "true-realignment-log-test.log"), "w")

	for patnum in args.participants:
		pat = "pat" + str(patnum)
		log.write(f"{pat}\n----------\n\n")

		patdir = os.path.join(outdir, pat)
		os.mkdir(patdir) 

		readsdir = os.path.join(subset_reads, pat) # readsdir = os.path.join(eek_reads, pat) # get path to reads directory based on input participant(s)
		reads = sorted(glob.glob(os.path.join(readsdir, "*"))) # get reads to run software on
		non_bladder_reads = filter_reads(reads, bladder_samples)

		bladder_mag = glob.glob(os.path.join(mags_path, pat, "Bladder*"))[0] # the bladder mag will be the only one in the directory with the Bladder prefix
		bt2_index = os.path.join(patdir, pat + "_bladder_map")

		build_index(bladder_mag, bt2_index)

		print(f"running bowtie on {pat}...") 
		run_bowtie(bt2_index, non_bladder_reads, args.threads, patdir, log)
		print(f"done\n")

	log.close()

	end = time.time()
	print(f"took {end - start} seconds")

	return

if __name__ == "__main__":
	main()

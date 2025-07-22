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
	parser.add_argument("-p", "--participants", nargs="+", required=True, help="get list of participants to align and assemble")
	parser.add_argument("-t", "--threads")
	parser.add_argument("-s", "--subset", action="store_true", help="run on test data (still uses pat numbers)")
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
	subprocess.run([ # build index to act as reference for bt2
		"bowtie2-build", "-q", mag, ind
	])

	return

def run_bowtie(ind, reads, proc, out, log):
	"""run bowtie, aligning each non-bladder read to the bladder mag using --very-fast heuristic"""
	for i in range(0, len(reads), 2):
		fread = reads[i]
		rread = reads[i+1]
		sample_num = os.path.split(fread)[1].split("_")[0]
		print(sample_num + "...")

		result = subprocess.run([
			"bowtie2",
			"--very-fast",
			"-p", proc,
			"-x", ind,
			"-1", fread,
			"-2", rread,
			"-S", os.path.join(out, sample_num + "_map.sam"),
			"--al-conc", os.path.join(out, sample_num + "_%.fq")
			],
			capture_output=True,
			text=True
		)

		log.write(f"{sample_num}:\n")

		for line in result.stderr.splitlines(): # write out percent alignment rate for each parameter
			if "overall alignment rate" in line:
				log.write(f"{line}\n\n")
	return

def run_spades(reads, proc, out, log):
	"""run spades, assembling reads that wrote out from bowtie"""
	for i in range(0, len(reads), 2):
		fread = reads[i]
		rread = reads[i+1]
		sample_num = os.path.split(fread)[1].split("_")[0]
		sample_out = os.path.join(out, sample_num)
		os.mkdir(sample_out)

		print(sample_num + "...")
		result = subprocess.run([
			"spades.py",
			"-1", fread,
			"-2", rread,
			"-t", proc,
			"-o", sample_out
			],
			capture_output=True
		)
	return

def run_fastani(contigs, pat, tmpdir, log):
	"""runs fastani pairwise for all assemblies in a given participant"""
	contigs_path_list = os.path.join(tmpdir, "contigs_path_list.txt")
	with open(contigs_path_list, "w") as f: # aggregate paths to contigs files to pass to fastani
		for path in contigs:
			f.write(f"{path}\n")

	fastani_out = os.path.join(tmpdir, f"fani_tmp_out_{pat}.txt")
	result = subprocess.run([
		"fastANI",
		"--ql", contigs_path_list,
		"--rl", contigs_path_list,
		"-o", fastani_out
		],
		capture_output=True,
		text=True
	)

	log.write(f"query\tref\tANI\n")
	with open(fastani_out) as f:
		for line in f.readlines():
			data = line.split("\t")
			query = data[0].split("/")[-2]
			query = "bMAG" if query.startswith("pat") else query
			reference = data[1].split("/")[-2]
			reference = "bMAG" if reference.startswith("pat") else reference
			ani = data[2]
			log.write(f"{query}\t{reference}\t{ani}\n")
	log.write("\n")
	return

def main():
	start = time.time() # how long does this take to run

	args = get_args(sys.argv[1:])
	threads = args.threads if args.threads else "16"

	outdir = os.path.abspath("output")
	if os.path.isdir(outdir):
		os.system(f"rm -r {outdir}")
	os.mkdir(outdir)
	tmpdir = os.path.join(outdir, "tmp")
	os.mkdir(tmpdir)
	log = open(os.path.join(outdir, "mag-realignment.log"), "w")

	if args.subset:
		eek_reads = "data/subset/" # if i want to run on test data
	else:
		eek_reads = "/media/catherine/Seagate/EEK/" # path to EEK directory, which contains all participant reads
	mags_path = "/media/catherine/Seagate/HPCC_Backup/aavalos4/making_mags/MAGS/" # path to Lexi's dir with the mags

	bladder_samples = get_bladder_samples()

	for patnum in args.participants:
		pat = "pat" + str(patnum)
		log.write(f"{pat}\n----------\n\n")

		patdir = os.path.join(outdir, pat)
		os.mkdir(patdir) 

		readsdir = os.path.join(eek_reads, pat) # get path to reads directory based on input participant(s)
		reads = sorted(glob.glob(os.path.join(readsdir, "*"))) # get reads to run software on
		non_bladder_reads = filter_reads(reads, bladder_samples)

		bladder_mag = glob.glob(os.path.join(mags_path, pat, "Bladder*"))[0] # the bladder mag will be the only one in the directory with the Bladder prefix

		bowtie_out = os.path.join(patdir, "bowtie2")
		os.mkdir(bowtie_out)

		bt2_index = os.path.join(bowtie_out, pat + "_map_ref")

		print(f"building index for {pat}...")
		build_index(bladder_mag, bt2_index)
		print(f"done\n")

		print(f"running bowtie on {pat}...") 
		run_bowtie(bt2_index, non_bladder_reads, threads, bowtie_out, log)
		print(f"done\n")

		spades_in = sorted(glob.glob(bowtie_out + "/*.fq"))
		spades_out = os.path.join(patdir, "spades")
		os.mkdir(spades_out)

		print(f"running spades on {pat}...")
		run_spades(spades_in, threads, spades_out, log)
		print(f"done\n")

		contigs_paths = glob.glob(os.path.join(outdir, "pat*/spades/*/contigs.fasta")) # paths to each contigs file from SPAdes run for this pat
		contigs_paths.append(bladder_mag)
		print(f"running fastani on {pat}...")
		run_fastani(contigs_paths, pat, tmpdir, log)
		print(f"done\n")

	end = time.time()
	print(f"took {end - start} seconds")
	log.write(f"took {end - start} seconds\n")

	log.close()

	return

if __name__ == "__main__":
	main()

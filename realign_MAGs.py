"""align reads against a MAG based on user input"""

import os
import sys
import glob
import argparse
import pandas as pd # type: ignore
import time

def get_args(args):
    """retrieve command line arguements"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reads", required=True)
    parser.add_argument("-m", "--mag", required=True)
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

def run_bowtie(mag, ind, reads, threads):
    print("building index...")
    os.system(f"bowtie2-build -q {mag} {ind}") # build index to act as reference for bt2
    print(f"done\n")

    proc = str(threads) if threads else "1"

    for i in range(1): # for i in range(0, len(reads), 2):
        sample_num = reads[i].split("/")[-1].split("_")[0]
        fread = reads[i]
        rread = reads[i+1]
        print(f"running bowtie on {sample_num}...")
        os.system(f"bowtie2 -p {proc} -x {ind} -1 {fread} -2 {rread} -S {sample_num}_map.sam --al-conc {sample_num}_%.fq")
        print(f"done\n")

def main():
    start = time.time() # how long does this take to run?

    args = get_args(sys.argv[1:])

    bladder_samples = get_bladder_samples()

    reads = sorted(glob.glob(f"{args.reads}/*"))
    non_bladder_reads = filter_reads(reads, bladder_samples)

    bladder_mag = args.mag
    pat = args.reads.split("/")[-2]
    bt2_index = pat + "_bladder_map"
    run_bowtie(bladder_mag, bt2_index, non_bladder_reads, args.threads)

    end = time.time()
    print(f"took {end - start} seconds")

if __name__ == "__main__":
    main()

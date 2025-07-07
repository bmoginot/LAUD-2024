"""run bowtie2 on the same read pair with different parameters to compare stringency"""

import os
import sys
import glob
import argparse
import subprocess

def get_args(args):
    """retrieve command line arguements"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reads", required=True)
    parser.add_argument("-m", "--mag", required=True)
    parser.add_argument("-t", "--threads")
    return parser.parse_args(args)

def build_index(mag, ind):
    print("building index...")

    subprocess.run([ # build index to act as reference for bt2
        "bowtie2-build", "-q",
        mag,
        ind
    ])

    print(f"done\n")

    return

def run_bowtie(ind, fread, rread, sample_num, threads, log):

    proc = str(threads) if threads else "1"

    params = ["--very-fast", "--fast", "--sensitive", "--very-sensitive"]

    for opt in params: # run bowtie on read pair with each stringency setting
        result = subprocess.run([
            "bowtie2",
            opt, # parameter affecting stringency
            "-p", proc,
            "-x", ind,
            "-1", fread,
            "-2", rread,
            "-S" f"output/{sample_num}_map.sam",
            "--al-conc", f"output/{sample_num}_%.fq"
            ],
            capture_output = True,
            text = True
        )

        log.write(f"{opt}:\n")
        for line in result.stderr.splitlines(): # write out percent alignment rate for each parameter
            if "overall alignment rate" in line:
                log.write(f"{line}\n\n")

def main():
    args = get_args(sys.argv[1:])

    if os.path.isdir("output"):
        os.system("rm -r output")

    os.mkdir("output")

    reads = sorted(glob.glob(f"{args.reads}/*"))
    pat = reads[0].split("/")[-2]

    log = open("mag-realignment.log", "w")

    bladder_mag = args.mag
    bt2_index = f"output/{pat}_bladder"

    build_index(bladder_mag, bt2_index)
    
    for i in range(0, len(reads), 2):
        sample_num = reads[i].split("/")[-1].split("_")[0] # get sample number to write to output
        log.write(f"{sample_num}\n\n")

        fread = reads[i]
        rread = reads[i+1]

        print(f"running {sample_num}...")
        run_bowtie(bt2_index, fread, rread, sample_num, args.threads, log)
        print(f"done\n")

    log.close()

if __name__ == "__main__":
    main()

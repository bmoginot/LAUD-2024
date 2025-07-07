"""run bowtie2 on the same read pair with different parameters to compare stringency"""

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

def run_bowtie(mag, ind, reads, threads, log):
    print("building index...")

    subprocess.run([ # build index to act as reference for bt2
        "bowtie2-build", "-q",
        mag,
        ind
    ])

    print(f"done\n")

    proc = str(threads) if threads else "1"

    sample_num = reads[0].split("/")[-1].split("_")[0]
    fread = reads[0]
    rread = reads[1]

    params = ["--very-fast", "--fast", "--sensitive", "--very-sensitive"]

    for opt in params:
        print(f"running bowtie2 with {opt}...")

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
        for line in result.stderr.splitlines():
            if "overall alignment rate" in line:
                log.write(f"{line}\n\n")

        print(f"done\n")

def main():
    args = get_args(sys.argv[1:])

    reads = sorted(glob.glob(f"{args.reads}/*"))

    log = open("mag-realignment.log", "w")

    bladder_mag = args.mag
    bt2_index = "output/pat17_bladder"
    run_bowtie(bladder_mag, bt2_index, reads, args.threads, log)

    log.close()

if __name__ == "__main__":
    main()

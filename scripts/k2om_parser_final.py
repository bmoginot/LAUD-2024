import os
import glob

# get the paths of the participants
fastq_list=sorted(glob.glob('/home/bmoginot/pat*'))

for path in fastq_list:
    # get directory name
    dir=path.split('/')[-1]
    # make directories for participant data
    os.system(f'mkdir /home/bmoginot/k2om_kfiles/{dir}')
    os.system(f'mkdir /home/bmoginot/k2om_kreports/{dir}')
    # get list of sample paths in given dir
    sample_paths=sorted(glob.glob(f'/home/bmoginot/{dir}/*'))
    # iterate through paired reads in dir
    for i in range(0, len(sample_paths), 2):
        # get path for each of paired reads
        l_sample=sample_paths[i]
        r_sample=sample_paths[i+1]
        # get the sample name
        sig=l_sample.split('/')[-1][:4]
        # create paths for kraken2 output
        kraken_path=f'/home/bmoginot/k2om_kfiles/{dir}/{sig}.out'
        kreport_path=f'/home/bmoginot/k2om_kreports/{dir}/{sig}.report'
        # run kraken
        os.system(f'kraken2 --db krakendb --paired {l_sample} {r_sample} --threads 8 --use-names --report {kreport_path} --report-zero-counts --output {kraken_path}')
    # get path for output dir from above command
    k2_pat_dir=f'/home/bmoginot/k2om_kreport/{dir}'
    # name output file for rarefaction
    k2om_outfile=f'/home/bmoginot/k2om_output/{dir}.out'
    # run rarefaction script to get tsv
    os.system(f'/home/bmoginot/Kraken2-output-manipulation/kraken-multiple.py -d {k2_pat_dir} -r S -c 2 -o {k2om_outfile}')
    # run bash command in terminal and read csv into R

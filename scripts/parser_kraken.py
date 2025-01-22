import os
import glob

# get the paths of the participants
fastq_list=sorted(glob.glob('/home/bmoginot/pat*'))

for path in fastq_list:
    # get directory name
    dir=path.split('/')[-1]
    # make directories for participant data
    os.system(f'mkdir /home/bmoginot/kfiles/{dir}')
    os.system(f'mkdir /home/bmoginot/kreports/{dir}')
    os.system(f'mkdir /home/bmoginot/bfiles/{dir}')
    os.system(f'mkdir /home/bmoginot/breports/{dir}')
    # get list of sample paths in given dir
    sample_paths=sorted(glob.glob(f'/home/bmoginot/{dir}/*'))
    # iterate through paired reads in dir
    for i in range(0,len(sample_paths),2):
        # get path for each of paired reads
        l_path=sample_paths[i]
        r_path=sample_paths[i+1]
        # get the sample name and remove file type
        sig=l_path.split('/')[-1].split('.')[0][:-7]
        # create paths for kraken2 output
        kraken_path=f'/home/bmoginot/kfiles/{dir}/{sig}'
        kreport_path=f'/home/bmoginot/kreports/{dir}/{sig}'
        # run kraken
        os.system(f'kraken2 --db krakendb --threads 8 --report {kreport_path}.k2report --report-minimizer-data --minimum-hit-groups 3 {l_path} {r_path} > {kraken_path}.kraken2')
        # create paths for bracken output
        bracken_path=f'/home/bmoginot/bfiles/{dir}/{sig}'
        breport_path=f'/home/bmoginot/breports/{dir}/{sig}'
        # run bracken
        os.system(f'bracken -d krakendb -i {kreport_path}.k2report -r 100 -l S -t 10 -o {bracken_path}.bracken -w {breport_path}.breport')

pat1=glob.glob('/home/bmoginot/pat1/*')
for i in range(0,len(pat1),2):
    l_sample=pat1[i]
    r_sample=pat1[i+1]
    sig=l_sample.split('/')[-1][:4]
    os.system(f'kraken2 --db krakendb --paired {l_sample} {r_sample} --threads 8 --use-names --report /home/bmoginot/k2$

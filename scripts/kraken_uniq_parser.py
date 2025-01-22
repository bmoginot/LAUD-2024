import os
import glob

sample_paths=glob.glob('/home/bmoginot/patdata/pat1/*')

for i in range(0,len(sample_paths),2):
    # get path for each of paired reads
    l_path=sample_paths[i]
    r_path=sample_paths[i+1]
    # get the sample name and remove file type
    sig=l_path.split('/')[-1].split('.')[0][:-7]
    # run kraken
    os.system(f'krakenuniq --db /home/bmoginot/kuniqdb --threads 10 --report-file {sig}_report.tsv {l_path} {r_path} > {sig}_class.tsv')

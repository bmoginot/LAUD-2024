import os
import glob

pat1=glob.glob('/home/bmoginot/pat1/*')
for i in range(0,len(pat1),2):
    l_sample=pat1[i]
    r_sample=pat1[i+1]
    sig=l_sample.split('/')[-1][:4]
    os.system(f'kraken2 --db krakendb --paired {l_sample} {r_sample} --threads 8 --use-names --report /home/bmoginot/k2om_kreports/{sig}.report --report-zero-counts --output /home/bmoginot/k2om_kfiles/{sig}.out')

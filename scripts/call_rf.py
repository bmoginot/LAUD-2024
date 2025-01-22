import os
import glob

paths = glob.glob('/home/bmoginot/new_kraken/filtered_reads/*')
for path in paths:
    pat = path.split('/')[-1][:-13]
    os.system(f'Rscript /home/bmoginot/scripts/rf_with_args.R --file {pat}')
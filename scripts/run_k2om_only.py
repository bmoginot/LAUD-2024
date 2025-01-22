import os
import glob

pats=sorted(glob.glob('/home/bmoginot/k2om_kreports/pat*'))
for pat in pats:
    dir=pat.split('/')[-1]
    out=f'/home/bmoginot/k2om_output/{dir}'
    os.system(f'/home/bmoginot/Kraken2-output-manipulation/kraken-multiple.py -d {pat} -r S -c 2 -o {out}')

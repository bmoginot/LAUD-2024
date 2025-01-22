import os
import glob

for i in range(2):
    mock_paths=glob.glob(f'/home/bmoginot/Mock{i+1}/*')
    os.system(f'kraken2 --db krakendb --threads 8 --report Mock{i+1}.k2report --report-minimizer-data --minimum-hit-groups 3 {mock_paths[0]} {mock_paths[1]} > Mock{i+1}.kraken2')

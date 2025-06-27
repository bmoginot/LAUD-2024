#! /bin/bash

for f in data/pat17/*
do
    filename=$(basename $f) # get just the name of the file, not the whole path
    out=${filename/fastq.gz/fq}
    zless $f | head -n 40000 > $out
done

#! /bin/bash

mag="data/Bladder_9023B_S23cleaned.fasta"
ind="pat17_subset"

printf "building index...\n"
bowtie2-build -q $mag $ind
printf "done\n\n"

fread="data/subset/9024R_S24_R1_001.fq"
rread="data/subset/9024R_S24_R2_001.fq"
threads="2"

params="--very-fast --fast --sensitive --very-sensitive"

echo > log.txt

for p in $params;
    do
    printf '%s\n\n' "$p" >> log.txt
    printf "running bowtie2 with $p\n"
    bowtie2 $p -p $threads -x $ind -1 $fread -2 $rread -S "test_map.sam" --al-conc "test_%.fq" &>> log.txt
    printf "done\n"
    done

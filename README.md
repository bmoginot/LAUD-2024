# LAUD 2024 Work for Dr. Putonti + 2025 MAG Realignment
## Kraken2 and Bracken Workflow
The main pipeline runs Kraken2 and Bracken on sequence reads from urinary microbiome samples. The final output is microbial species occurence for each participant's samples.

### Steps
1. *Build Kraken2 database.* Kraken2 needs to download a microbial reference database before it can run. The script helps to build that.
2. *Generate kraken reports.* Kraken2 identifies microbial taxa present in each sample.
3. *Generate bracken reports.* Bracken estimates relative abundance of taxa identified by Kraken2.
4. *Find recurrent species.* The script parses Bracken files, compares samples to metadata, and finds which taxa occur in more than one sample across each participant.

## MAG Realignment
After building the above pipeline, we re-aligned reads from certain participants and re-assembled those sequences.

### Steps
1. *Identify aberrant participants.* Lexi found several pats whose MAGs may be representative of >1 species rather than just E. coli. Many of these are apparent in the text of her thesis and include pats 3, 17, and 20.
2. *Retrieve participant data.* Next, the reads for these aberrant participants were collected. These reads are to be aligned against the bladder MAG, so that was collect as well. Since the bladder MAG is the reference, any reads that originated from bladder samples were ignored. So, for each participant, we had non-bladder read pairs + a bladder MAG.
3. *Align with Bowtie2*. The bladder MAG was used to build a Bowtie2 index. This index was passed to bowtie along with each pair of reads. The reads were aligned against the index and any reads that aligned were written out. Since we expect that some non-E.-coli reads were previously being aligned, we changed the pre-set heuristic from `--sensitive` to `--very-fast`. This resulted in fewer reads aligning to the index, which hopefully were these non-E.-coli reads. This process was performed for each chosen participant with their own data and bladder MAG.
4. *Assembly with SPAdes*. The aligned reads are then assembled by SPAdes using default parameters. A fasta file containing contigs is generated for each read pair. These constitute the new MAGs for each sample.
5. *ANI calculation*. For each participant, the MAGs (+ the old bladder MAG) are compared piece-wise against each other. In each comparison, the genetic distance is calculated. This gives an idea of how similar the newly generated MAGs are to each other. ANI values that are significantly low are not written out. If this is the case, we would assume that one of the MAGs is not E. coli.

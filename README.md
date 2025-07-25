# Work for Dr. Putonti to Finish Up Lexi's Thesis (Summer 2025)

This project is two-fold

## MAG Realignment
The first aim is to re-align reads from certain participants and re-assemble those sequences

### Steps
1. *Identify aberrant participants.* Lexi found several pats whose MAGs may be representative of >1 species rather than just E. coli. Many of these are apparent in the text of her thesis and include pats 3, 17, and 20.
2. *Retrieve participant data.* Next, the reads for these aberrant participants were collected. These reads are to be aligned against the bladder MAG, so that was collect as well. Since the bladder MAG is the reference, any reads that originated from bladder samples were ignored. So, for each participant, we had non-bladder read pairs + a bladder MAG.
3. *Align with Bowtie2*. The bladder MAG was used to build a Bowtie2 index. This index was passed to bowtie along with each pair of reads. The reads were aligned against the index and any reads that aligned were written out. Since we expect that some non-E.-coli reads were previously being aligned, we changed the pre-set heuristic from `--sensitive` to `--very-fast`. This resulted in fewer reads aligning to the index, which hopefully were these non-E.-coli reads. This process was performed for each chosen participant with their own data and bladder MAG.
4. *Assembly with SPAdes*. The aligned reads are then assembled by SPAdes using default parameters. A fasta file containing contigs is generated for each read pair. These constitute the new MAGs for each sample.
5. *ANI calculation*. For each participant, the MAGs (+ the old bladder MAG) are compared piece-wise against each other. In each comparison, the genetic distance is calculated. This gives an idea of how similar the newly generated MAGs are to each other. ANI values that are significantly low are not written out. If this is the case, we would assume that one of the MAGs is not E. coli.

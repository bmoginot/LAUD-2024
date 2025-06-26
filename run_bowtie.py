# sftp catherine@10.23.19.202
# in Lexi's home dir: /media/catherine/Seagate/HPCC_Backup/aavalos4/

# we're going to look at pat 17

# grabbed the MAG: 
# mv making_mags/MAGS/Bladder_9023B_S23cleaned.fasta pat17_bladder_MAG.fa

# grabbed the non-bladder reads from /media/catherine/Seagate/EEK/pat17
# 9023, 9027, and 9032 are bladder reads (per the EEK metadata)
# the only bladder reads in the dir were 9023, so i downloaded everything and deleted those.

import os
import glob

bowtie2-build pat17_bladder_MAG.fa pat17_bladder
bowtie2 -p 12 -x pat17_bladder -1 pat17/9024R_S24_R1_001.fastq.gz -2 pat17/9024R_S24_R2_001.fastq.gz -S 9024R_S24_map.sam
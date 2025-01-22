import os
import glob
import pandas as pd

def run_kraken(pat):
    # get paths to all samples from participant 1
    paths = sorted(glob.glob(f'/home/bmoginot/{pat}/*'))
    # iterate through paths
    for i in range(0, len(paths), 2):
        # get paths to paired reads
        l_sample = paths[i]
        r_sample = paths[i+1]
        # get sample number to name outfiles
        sig = l_sample.split('/')[-1][:4]
        # create paths for kraken2 output
        kraken_path = f'/home/bmoginot/new_kraken/k2om_kfiles/{pat}/{sig}.out'
        kreport_path = f'/home/bmoginot/new_kraken/k2om_kreports/{pat}/{sig}.report'
        # run kraken per k2om specificiations
        os.system(f'kraken2 --db /home/bmoginot/krakendb --paired {l_sample} {r_sample} --threads 8 --use-names --report {kreport_path} --report-zero-counts --output {kraken_path}')
    return

def run_k2om(pat):
    # get path for output dir from above command
    k2_pat_dir = f'/home/bmoginot/new_kraken/k2om_kreports/{pat}'
    # name output file for rarefaction
    k2om_outfile = f'/home/bmoginot/new_kraken/k2om_output/{pat}'
    # run rarefaction script to get tsv
    os.system(f'/home/bmoginot/Kraken2-output-manipulation/kraken-multiple.py -d {k2_pat_dir} -r S -c 2 -o {k2om_outfile}')
    # run bash command in terminal and read csv into R
    os.system(f'/home/bmoginot/scripts/{pat}_to_csv.sh')
    return

def filter_reads(file):
    # read in pat csv
    df = pd.read_csv(file)
    # format index
    df.index = df['TaxaID']
    df.drop('TaxaID', axis=1, inplace=True)
    # drop values less than 20
    df = df[df>20].fillna(0).astype(int)
    return df

def group_by_location(df, eek):
    # iterat through columns and change to just sample number
    new_cols = []
    for col in df.columns:
        sample_num = col.split('/')[-1][:4]
        new_cols += [sample_num]
    df.columns = new_cols
    # key dict with sample number and add cols with the same location
    locale_list = []
    for col in df.columns:
        locale = eek[int(col)]
        try:
            df[locale] += df[col]
        except KeyError:
            df[locale] = df[col]
            locale_list += [locale]
    # subset for only locations
    by_locale = df[locale_list]
    return by_locale

def write_out(file, df):
    # get file name
    name = file.split('/')[-1][:-4]
    # write out to csv
    df.to_csv(f'/home/bmoginot/new_kraken/filtered_reads/{name}_filtered.csv')
    return

def group_reads(pat):
    # get all csv files from k2om
    csv = f'/home/bmoginot/new_kraken/k2om_output/{pat}.csv'
    # i don't think the EEK xlsx file is on the remote server... so heres the dict i was going to make with it; makes little difference
    eek = {8327: 'bladder', 8328: 'Periurethral', 8329: 'vagina', 8330: 'rectal', 8331: 'bladder', 8332: 'Periurethral', 8333: 'vagina', 8334: 'rectal', 8335: 'bladder', 8336: 'Periurethral', 8337: 'vagina', 8338: 'rectal', 8376: 'bladder', 8377: 'Periurethral', 8378: 'vagina', 8379: 'rectal', 8380: 'bladder', 8381: 'Periurethral', 8382: 'vagina', 8383: 'rectal', 8384: 'bladder', 8385: 'Periurethral', 8386: 'vagina', 8387: 'rectal', 8415: 'bladder', 8416: 'rectal', 8417: 'Periurethral', 8418: 'vagina', 8419: 'bladder', 8420: 'rectal', 8421: 'Periurethral', 8422: 'vagina', 8423: 'bladder', 8424: 'rectal', 8425: 'Periurethral', 8426: 'vagina', 8431: 'bladder', 8432: 'rectal', 8433: 'Periurethral', 8434: 'vagina', 8435: 'bladder', 8436: 'rectal', 8437: 'Periurethral', 8438: 'vagina', 8439: 'bladder', 8440: 'rectal', 8441: 'Periurethral', 8442: 'vagina', 8488: 'bladder', 8489: 'rectal', 8490: 'Periurethral', 8491: 'vagina', 8492: 'bladder', 8493: 'rectal', 8494: 'Periurethral', 8495: 'vagina', 8496: 'bladder', 8497: 'rectal', 8498: 'Periurethral', 8499: 'vagina', 8517: 'bladder', 8518: 'rectal', 8519: 'Periurethral', 8520: 'vagina', 8521: 'bladder', 8522: 'rectal', 8523: 'Periurethral', 8524: 'vagina', 8525: 'bladder', 8526: 'rectal', 8527: 'Periurethral', 8528: 'vagina', 8596: 'bladder', 8597: 'rectal', 8598: 'Periurethral', 8599: 'vagina', 8600: 'bladder', 8601: 'rectal', 8602: 'Periurethral', 8603: 'vagina', 8604: 'bladder', 8605: 'rectal', 8606: 'Periurethral', 8607: 'vagina', 8622: 'cath', 8623: 'rectal', 8624: 'Periurethral', 8625: 'vagina', 8626: 'cath', 8627: 'rectal', 8628: 'Periurethral', 8629: 'vagina', 8630: 'cath', 8631: 'rectal', 8632: 'Periurethral', 8633: 'vagina', 8777: 'bladder', 8778: 'rectal', 8779: 'Periurethral', 8780: 'VAGINAL', 8781: 'bladder', 8782: 'rectal', 8783: 'Periurethral', 8784: 'VAGINAL', 8785: 'bladder', 8786: 'rectal', 8787: 'Periurethral', 8788: 'VAGINAL', 9023: 'bladder', 9024: 'rectal', 9025: 'Periurethral', 9026: 'VAGINA', 9027: 'bladder', 9028: 'rectal', 9029: 'Periurethral', 9030: 'VAGINA', 9031: 'bladder', 9032: 'rectal', 9033: 'Periurethral', 9034: 'VAGINA', 9067: 'bladder', 9068: 'Periurethral', 9069: 'rectal', 9070: 'VAGINA', 9071: 'bladder', 9072: 'Periurethral', 9073: 'bladder', 9074: 'Urethral', 9075: 'bladder', 9076: 'Periurethral', 9077: 'rectal', 9078: 'VAGINA', 9115: 'bladder', 9116: 'rectal', 9117: 'Periurethral', 9118: 'VAGINA', 9119: 'bladder', 9120: 'rectal', 9121: 'Periurethral', 9122: 'VAGINA', 9123: 'bladder', 9124: 'rectal', 9125: 'Periurethral', 9126: 'VAGINA', 9207: 'bladder', 9208: 'rectal', 9209: 'Periurethral', 9210: 'VAGINA', 9211: 'bladder', 9212: 'rectal', 9213: 'Periurethral', 9214: 'VAGINA', 9215: 'bladder', 9216: 'rectal', 9217: 'Periurethral', 9218: 'VAGINA', 9230: 'bladder', 9231: 'rectal', 9232: 'Periurethral', 9233: 'VAGINA', 9234: 'bladder', 9235: 'rectal', 9236: 'Periurethral', 9237: 'VAGINA', 9238: 'bladder', 9239: 'rectal', 9240: 'Periurethral', 9241: 'VAGINA', 9504: 'BLADDER', 9505: 'rectal', 9506: 'Periurethral', 9507: 'VAGINA', 9508: 'BLADDER', 9509: 'rectal', 9510: 'Periurethral', 9511: 'VAGINA', 9512: 'BLADDER', 9513: 'rectal', 9514: 'Periurethral', 9515: 'VAGINA', 9630: 'bladder', 9631: 'rectal', 9632: 'Periurethral', 9633: 'VAGINA', 9634: 'bladder', 9635: 'rectal', 9636: 'Periurethral', 9637: 'VAGINA', 9638: 'bladder', 9639: 'rectal', 9640: 'Periurethral', 9641: 'VAGINA', 9713: 'BLADDER', 9714: 'rectal', 9715: 'Periurethral', 9716: 'VAGINA', 9717: 'BLADDER', 9718: 'rectal', 9719: 'Periurethral', 9720: 'VAGINA', 9721: 'BLADDER', 9722: 'rectal', 9723: 'Periurethral', 9724: 'VAGINA', 9729: 'bladder', 9730: 'rectal', 9731: 'Periurethral', 9732: 'VAGINA', 9733: 'bladder', 9734: 'rectal', 9735: 'Periurethral', 9736: 'VAGINA', 9737: 'bladder', 9738: 'rectal', 9739: 'Periurethral', 9740: 'VAGINA', 9754: 'bladder', 9755: 'rectal', 9756: 'Periurethral', 9757: 'VAGINA', 9758: 'bladder', 9759: 'rectal', 9760: 'Periurethral', 9761: 'VAGINA', 9762: 'bladder', 9763: 'rectal', 9764: 'Periurethral', 9765: 'VAGINA', 9774: 'bladder', 9775: 'rectal', 9776: 'Periurethral', 9777: 'VAGINA', 9778: 'bladder', 9779: 'rectal', 9780: 'Periurethral', 9781: 'VAGINA', 9782: 'bladder', 9783: 'rectal', 9784: 'Periurethral', 9785: 'VAGINA', 9923: 'bladder', 9924: 'rectal', 9925: 'Periurethral', 9926: 'VAGINA', 9927: 'bladder', 9928: 'rectal', 9929: 'Periurethral', 9930: 'VAGINA', 9931: 'bladder', 9932: 'rectal', 9933: 'Periurethral', 9934: 'VAGINA'}
    # filter reads and group by location
    filtered_reads = filter_reads(csv)
    reads_by_location = group_by_location(filtered_reads, eek)
    # write to csv
    write_out(csv, reads_by_location)
    return
    
'''
This is a wrapper for all of the steps that convert participant fasta files to rarefaction curves, checking our sequence depth
1. Kraken2 compares all paired fasta files for a given participant against a bacterial sequence database and produces kraken2 reports
2. Report files for each sample are manipulated and converted to a csv file via a python script and a bash command; this file
   contains all of the species detected in each sample and the number of reads assigned to them
3. The csv is then filtered and samples are group together based on anatomical location from which they were isolated
4. This csv is then run through an R script which plots a rarefaction curve for each anatomical location
'''

def main():
    # set participant on which to run kraken
    pat = 'pat1'
    # run kraken on participant
    run_kraken(pat)
    # manipulate sample reads and output as csv
    run_k2om(pat)
    # filter reads and group samples by location
    group_reads(pat)
    # run rarefaction on grouped reads
    os.system(f'Rscript /home/bmoginot/scripts/rf_with_args.R --file {pat}')
    return

if __name__ == main():
    main()
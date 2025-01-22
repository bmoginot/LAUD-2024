import pandas as pd

# read in tsv containing ANI information as dataframe
df = pd.read_csv('/home/bmoginot/ani_files/fastANI_all_pat.tsv', sep='\t', header=None)
# get number of rows in the dataframe
rows = int(df.size / len(df.columns))
# iterate through each row of the dataframe
for i in range(rows):
    # get the names of the files being compared and isolate participant number
    pat0 = df[0][i].split('/')[4]
    pat1 = df[1][i].split('/')[4]
    ani = float(df[2][i])
    reads = int(df[3][i])
    # if both files are from the same participant, drop that row
    if pat0 == pat1:
        df.drop(i, inplace=True)
    elif ani < 95:
        df.drop(i, inplace=True)
    elif reads < 1000:
        df.drop(i, inplace=True)
# write cleaned output to tsv
df.to_csv('/home/bmoginot/ani_files/fastANI_reads.tsv', sep='\t')
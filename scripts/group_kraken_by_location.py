import pandas as pd

# read in k2om file
file='/home/bmoginot/new_kraken/k2om_output/pat1.csv'
col_names=pd.Index(['8330','8327','8334','8335','8331','8338'])
df=pd.read_csv(file,header=0,names=col_names)

# zero out cells with reads <20
df=df[df>20].fillna(0).astype(int)

# divide reads by anatomical location
df['bladder']=df['8327']+df['8335']+df['8331']
df['rectal']=df['8330']+df['8334']+df['8338']
by_location=df[['bladder','rectal']]
by_location.index.rename('TaxID',inplace=True)

# write out
by_location.to_csv('/home/bmoginot/pat1_filtered.csv')

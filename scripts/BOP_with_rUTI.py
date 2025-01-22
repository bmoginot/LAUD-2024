import glob
import pandas as pd

def get_top_species(paths):
    # iterate through files and create list of species present in each sample
    species_list = []
    head = pd.Index(['perc_coverage', 'frag_coverage', 'num_fragments', 'rank_code', 'taxID', 'name'])
    for path in paths:
        file = path
        # read in csv of given file
        df = pd.read_csv(file, sep='\t', names=head)
        # filter dataframe for species
        species = df[df['rank_code']=='S']
        # filter for species with coverage greater than 5%
        target_coverage = species[species['perc_coverage']>=5]
        # get names of taxa that meet above criteria
        names = target_coverage['name']
        # strip whitespace and add species to a list
        stripped_s = [s.strip() for s in names]
        # append list to list of species
        species_list.append(stripped_s)
    return species_list

def write_out(r, a):
    file = '/home/bmoginot/new_kraken/bracken_ruti.txt'
    with open(file, 'w') as f:
        f.write('recurrent: ')
        for s in r:
            f.write(s + ', ')
        f.write('\nacute: ')
        for s in a:
            f.write(s + ', ')

def main():
    # get the path for each participant directory
    dirs = glob.glob(f'/home/bmoginot/old_kraken/breports/*')
    # make dict for recurrent and acute UTI
    ruti = ['pat1', 'pat2', 'pat3', 'pat10', 'pat11', 'pat14', 'pat17', 'pat18', 'pat20', 'pat22', 'pat27', 'pat32', 'pat33', 'pat34', 'pat35']
    # lists for uti category
    recurrent = []
    acute = []
    # iterate through samples for each participant
    for pat in dirs:
        # get the directory name
        pat_dir = pat.split('/')[-1]
        # get the path for each sample for a given participant
        paths = glob.glob(f'{pat}/*')
        # get a list of lists containing top species for each sample
        species_list = get_top_species(paths)
        # get all species for the participant, removing redundances between samples
        species_per_pat = list(set([s for l in species_list for s in l if s]))
        # bin species by uti category
        if pat_dir in ruti:
            for s in species_per_pat:
                if s not in recurrent:
                    recurrent += [s]
        else:
            for s in species_per_pat:
                if s not in acute:
                    acute += [s]
    write_out(recurrent, acute)

if __name__ == '__main__':
    main()
# parse through each participant file, retrieving bracken report for each sample
# for each participant, compare the samples and determine which species are
# present across more than one sample at a coverage >= 5%
# create a text doc showing the samples in which the given species occur
# along with the culturing medium and isolation location for each sample

import pandas as pd
import glob

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

def make_dict(samples_list, species_list):
    # create dictionary mapping species to samples where they are found
    recurrent={}
    # iterate through species lists, doing pairwise comparisons
    for i in range(len(species_list)-1):
        current = species_list[i]
        for j in range(i+1, len(species_list)):
            samples = [samples_list[i], samples_list[j]]
            listy = [s for s in current if s in species_list[j]]
            # add species to dictionary with current samples as value
            # if present, append list of samples to value
            for s in listy:
                if s in recurrent:
                    recurrent[s] += samples
                else:
                    recurrent[s] = samples
    # remove redundancies
    recurrent = {k: set(recurrent[k]) for k in recurrent.keys()}
    return recurrent

def write_out(pat_dir,recurrent):
    path = f'/home/bmoginot/bracken_tests/{pat_dir}.txt'
    # write species and sample number and accompanying medium and location
    with open(path, 'w') as file:
        for k, v in recurrent.items():
            file.write(str(k) + ': ' + str(v) + '\n')

def main():
    # get the path for each participant directory
    dirs = glob.glob(f'/home/bmoginot/old_kraken/breports/*')
    # make dictionary to get medium and isolation location for samples
    reference_dict = {'PST': {8327: 'LB', 8328: 'LB', 8329: 'LB', 8330: 'LB', 8331: 'NYC', 8332: 'NYC', 8333: 'NYC', 8334: 'NYC', 8335: 'LIM', 8336: 'LIM', 8337: 'LIM', 8338: 'LIM', 8376: 'LB', 8377: 'LB', 8378: 'LB', 8379: 'LB', 8380: 'LIM', 8381: 'LIM', 8382: 'LIM', 8383: 'LIM', 8384: 'NYC', 8385: 'NYC', 8386: 'NYC', 8387: 'NYC', 8415: 'LB RT', 8416: 'LB RT', 8417: 'LB RT', 8418: 'LB RT', 8419: 'LIM', 8420: 'LIM', 8421: 'LIM', 8422: 'LIM', 8423: 'NYC-N', 8424: 'NYC-N', 8425: 'NYC-N', 8426: 'NYC-N', 8431: 'LB RT', 8432: 'LB RT', 8433: 'LB RT', 8434: 'LB RT', 8435: 'LIM', 8436: 'LIM', 8437: 'LIM', 8438: 'LIM', 8439: 'NYC-N', 8440: 'NYC-N', 8441: 'NYC-N', 8442: 'NYC-N', 8488: 'LB RT', 8489: 'LB RT', 8490: 'LB RT', 8491: 'LB RT', 8492: 'LIM', 8493: 'LIM', 8494: 'LIM', 8495: 'LIM', 8496: 'NYC-NC', 8497: 'NYC-NC', 8498: 'NYC-NC', 8499: 'NYC-NC', 8517: 'LB RT', 8518: 'LB RT', 8519: 'LB RT', 8520: 'LB RT', 8521: 'LIM', 8522: 'LIM', 8523: 'LIM', 8524: 'LIM', 8525: 'NYC-NC', 8526: 'NYC-NC', 8527: 'NYC-NC', 8528: 'NYC-NC', 8596: 'LB RT', 8597: 'LB RT', 8598: 'LB RT', 8599: 'LB RT', 8600: 'LIM', 8601: 'LIM', 8602: 'LIM', 8603: 'LIM', 8604: 'NYC-NC', 8605: 'NYC-NC', 8606: 'NYC-NC', 8607: 'NYC-NC', 8622: 'LBRT', 8623: 'LBRT', 8624: 'LBRT', 8625: 'LBRT', 8626: 'LIM', 8627: 'LIM', 8628: 'LIM', 8629: 'LIM', 8630: 'NYC-NC', 8631: 'NYC-NC', 8632: 'NYC-NC', 8633: 'NYC-NC', 8777: 'LB RT', 8778: 'LB RT', 8779: 'LB RT', 8780: 'LB RT', 8781: 'LIM', 8782: 'LIM', 8783: 'LIM', 8784: 'LIM', 8785: 'NYC-NC', 8786: 'NYC-NC', 8787: 'NYC-NC', 8788: 'NYC-NC', 9023: 'LB RT', 9024: 'LB RT', 9025: 'LB RT', 9026: 'LB RT', 9027: 'LIM', 9028: 'LIM', 9029: 'LIM', 9030: 'LIM', 9031: 'NYC-NC', 9032: 'NYC-NC', 9033: 'NYC-NC', 9034: 'NYC-NC', 9067: 'LB RT', 9068: 'LB RT', 9069: 'LB RT', 9070: 'LB RT', 9071: 'LIM', 9072: 'LIM', 9073: 'LIM', 9074: 'LIM', 9075: 'NYC-NC', 9076: 'NYC-NC', 9077: 'NYC-NC', 9078: 'NYC-NC', 9115: 'LB RT', 9116: 'LB RT', 9117: 'LB RT', 9118: 'LB RT', 9119: 'LIM', 9120: 'LIM', 9121: 'LIM', 9122: 'LIM', 9123: 'NYC-NC', 9124: 'NYC-NC', 9125: 'NYC-NC', 9126: 'NYC-NC', 9207: 'LB RT', 9208: 'LB RT', 9209: 'LB RT', 9210: 'LB RT', 9211: 'LIM', 9212: 'LIM', 9213: 'LIM', 9214: 'LIM', 9215: 'NYC-NC', 9216: 'NYC-NC', 9217: 'NYC-NC', 9218: 'NYC-NC', 9230: 'LB RT', 9231: 'LB RT', 9232: 'LB RT', 9233: 'LB RT', 9234: 'LIM', 9235: 'LIM', 9236: 'LIM', 9237: 'LIM', 9238: 'NYC-NC', 9239: 'NYC-NC', 9240: 'NYC-NC', 9241: 'NYC-NC', 9504: 'LBRT', 9505: 'LBRT', 9506: 'LBRT', 9507: 'LBRT', 9508: 'LIM', 9509: 'LIM', 9510: 'LIM', 9511: 'LIM', 9512: 'NYC-NC', 9513: 'NYC-NC', 9514: 'NYC-NC', 9515: 'NYC-NC', 9630: 'LBRT', 9631: 'LBRT', 9632: 'LBRT', 9633: 'LBRT', 9634: 'LIM', 9635: 'LIM', 9636: 'LIM', 9637: 'LIM', 9638: 'NYCNC', 9639: 'NYCNC', 9640: 'NYCNC', 9641: 'NYCNC', 9713: 'LBRT', 9714: 'LBRT', 9715: 'LBRT', 9716: 'LBRT', 9717: 'LIM', 9718: 'LIM', 9719: 'LIM', 9720: 'LIM', 9721: 'NYCNC', 9722: 'NYCNC', 9723: 'NYCNC', 9724: 'NYCNC', 9729: 'LBRT', 9730: 'LBRT', 9731: 'LBRT', 9732: 'LBRT', 9733: 'LIM', 9734: 'LIM', 9735: 'LIM', 9736: 'LIM', 9737: 'NYCNC', 9738: 'NYCNC', 9739: 'NYCNC', 9740: 'NYCNC', 9754: 'LBRT', 9755: 'LBRT', 9756: 'LBRT', 9757: 'LBRT', 9758: 'LIM', 9759: 'LIM', 9760: 'LIM', 9761: 'LIM', 9762: 'NYCNC', 9763: 'NYCNC', 9764: 'NYCNC', 9765: 'NYCNC', 9774: 'LB', 9775: 'LB', 9776: 'LB', 9777: 'LB', 9778: 'LIM', 9779: 'LIM', 9780: 'LIM', 9781: 'LIM', 9782: 'NYCNC', 9783: 'NYCNC', 9784: 'NYCNC', 9785: 'NYCNC', 9923: 'LBRT', 9924: 'LBRT', 9925: 'LBRT', 9926: 'LBRT', 9927: 'LIM', 9928: 'LIM', 9929: 'LIM', 9930: 'LIM', 9931: 'NYCNC', 9932: 'NYCNC', 9933: 'NYCNC', 9934: 'NYCNC'}, 'SL': {8327: 'bladder', 8328: 'Periurethral', 8329: 'vagina', 8330: 'rectal', 8331: 'bladder', 8332: 'Periurethral', 8333: 'vagina', 8334: 'rectal', 8335: 'bladder', 8336: 'Periurethral', 8337: 'vagina', 8338: 'rectal', 8376: 'bladder', 8377: 'Periurethral', 8378: 'vagina', 8379: 'rectal', 8380: 'bladder', 8381: 'Periurethral', 8382: 'vagina', 8383: 'rectal', 8384: 'bladder', 8385: 'Periurethral', 8386: 'vagina', 8387: 'rectal', 8415: 'bladder', 8416: 'rectal', 8417: 'Periurethral', 8418: 'vagina', 8419: 'bladder', 8420: 'rectal', 8421: 'Periurethral', 8422: 'vagina', 8423: 'bladder', 8424: 'rectal', 8425: 'Periurethral', 8426: 'vagina', 8431: 'bladder', 8432: 'rectal', 8433: 'Periurethral', 8434: 'vagina', 8435: 'bladder', 8436: 'rectal', 8437: 'Periurethral', 8438: 'vagina', 8439: 'bladder', 8440: 'rectal', 8441: 'Periurethral', 8442: 'vagina', 8488: 'bladder', 8489: 'rectal', 8490: 'Periurethral', 8491: 'vagina', 8492: 'bladder', 8493: 'rectal', 8494: 'Periurethral', 8495: 'vagina', 8496: 'bladder', 8497: 'rectal', 8498: 'Periurethral', 8499: 'vagina', 8517: 'bladder', 8518: 'rectal', 8519: 'Periurethral', 8520: 'vagina', 8521: 'bladder', 8522: 'rectal', 8523: 'Periurethral', 8524: 'vagina', 8525: 'bladder', 8526: 'rectal', 8527: 'Periurethral', 8528: 'vagina', 8596: 'bladder', 8597: 'rectal', 8598: 'Periurethral', 8599: 'vagina', 8600: 'bladder', 8601: 'rectal', 8602: 'Periurethral', 8603: 'vagina', 8604: 'bladder', 8605: 'rectal', 8606: 'Periurethral', 8607: 'vagina', 8622: 'cath', 8623: 'rectal', 8624: 'Periurethral', 8625: 'vagina', 8626: 'cath', 8627: 'rectal', 8628: 'Periurethral', 8629: 'vagina', 8630: 'cath', 8631: 'rectal', 8632: 'Periurethral', 8633: 'vagina', 8777: 'bladder', 8778: 'rectal', 8779: 'Periurethral', 8780: 'VAGINAL', 8781: 'bladder', 8782: 'rectal', 8783: 'Periurethral', 8784: 'VAGINAL', 8785: 'bladder', 8786: 'rectal', 8787: 'Periurethral', 8788: 'VAGINAL', 9023: 'bladder', 9024: 'rectal', 9025: 'Periurethral', 9026: 'VAGINA', 9027: 'bladder', 9028: 'rectal', 9029: 'Periurethral', 9030: 'VAGINA', 9031: 'bladder', 9032: 'rectal', 9033: 'Periurethral', 9034: 'VAGINA', 9067: 'bladder', 9068: 'Periurethral', 9069: 'rectal', 9070: 'VAGINA', 9071: 'bladder', 9072: 'Periurethral', 9073: 'bladder', 9074: 'Urethral', 9075: 'bladder', 9076: 'Periurethral', 9077: 'rectal', 9078: 'VAGINA', 9115: 'bladder', 9116: 'rectal', 9117: 'Periurethral', 9118: 'VAGINA', 9119: 'bladder', 9120: 'rectal', 9121: 'Periurethral', 9122: 'VAGINA', 9123: 'bladder', 9124: 'rectal', 9125: 'Periurethral', 9126: 'VAGINA', 9207: 'bladder', 9208: 'rectal', 9209: 'Periurethral', 9210: 'VAGINA', 9211: 'bladder', 9212: 'rectal', 9213: 'Periurethral', 9214: 'VAGINA', 9215: 'bladder', 9216: 'rectal', 9217: 'Periurethral', 9218: 'VAGINA', 9230: 'bladder', 9231: 'rectal', 9232: 'Periurethral', 9233: 'VAGINA', 9234: 'bladder', 9235: 'rectal', 9236: 'Periurethral', 9237: 'VAGINA', 9238: 'bladder', 9239: 'rectal', 9240: 'Periurethral', 9241: 'VAGINA', 9504: 'BLADDER', 9505: 'rectal', 9506: 'Periurethral', 9507: 'VAGINA', 9508: 'BLADDER', 9509: 'rectal', 9510: 'Periurethral', 9511: 'VAGINA', 9512: 'BLADDER', 9513: 'rectal', 9514: 'Periurethral', 9515: 'VAGINA', 9630: 'bladder', 9631: 'rectal', 9632: 'Periurethral', 9633: 'VAGINA', 9634: 'bladder', 9635: 'rectal', 9636: 'Periurethral', 9637: 'VAGINA', 9638: 'bladder', 9639: 'rectal', 9640: 'Periurethral', 9641: 'VAGINA', 9713: 'BLADDER', 9714: 'rectal', 9715: 'Periurethral', 9716: 'VAGINA', 9717: 'BLADDER', 9718: 'rectal', 9719: 'Periurethral', 9720: 'VAGINA', 9721: 'BLADDER', 9722: 'rectal', 9723: 'Periurethral', 9724: 'VAGINA', 9729: 'bladder', 9730: 'rectal', 9731: 'Periurethral', 9732: 'VAGINA', 9733: 'bladder', 9734: 'rectal', 9735: 'Periurethral', 9736: 'VAGINA', 9737: 'bladder', 9738: 'rectal', 9739: 'Periurethral', 9740: 'VAGINA', 9754: 'bladder', 9755: 'rectal', 9756: 'Periurethral', 9757: 'VAGINA', 9758: 'bladder', 9759: 'rectal', 9760: 'Periurethral', 9761: 'VAGINA', 9762: 'bladder', 9763: 'rectal', 9764: 'Periurethral', 9765: 'VAGINA', 9774: 'bladder', 9775: 'rectal', 9776: 'Periurethral', 9777: 'VAGINA', 9778: 'bladder', 9779: 'rectal', 9780: 'Periurethral', 9781: 'VAGINA', 9782: 'bladder', 9783: 'rectal', 9784: 'Periurethral', 9785: 'VAGINA', 9923: 'bladder', 9924: 'rectal', 9925: 'Periurethral', 9926: 'VAGINA', 9927: 'bladder', 9928: 'rectal', 9929: 'Periurethral', 9930: 'VAGINA', 9931: 'bladder', 9932: 'rectal', 9933: 'Periurethral', 9934: 'VAGINA'}}
    # iterate through samples for each participant
    for pat in dirs:
        # get the directory name
        pat_dir = pat.split('/')[-1]
        # get the path for each sample for a given participant
        paths = glob.glob(f'/home/bmoginot/old_kraken/breports/{pat_dir}/*')
        # get a list of lists containing top species for each sample
        species_list = get_top_species(paths)
        # get list of sample names
        split_paths = [l.split('/') for l in paths]
        samples_list = [s[-1][:4] for s in split_paths]
        # get dictionary with species: samples
        recurrent = make_dict(samples_list, species_list)
        # take sample numbers and determine the medium and isolation location
        # for the given sample and recontruct the dictionary with a list of lists
        # containing sample numbers, media, and locations
        for species in recurrent.keys():
            # crazy fucking list comprehension:
            recurrent[species] = [[num, reference_dict['PST'][int(num)], reference_dict['SL'][int(num)]] for num in recurrent[species]]
        # write out to text file
        write_out(pat_dir,recurrent)

if __name__ == '__main__':
    main()
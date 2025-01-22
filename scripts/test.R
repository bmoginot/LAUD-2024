library(argparse)

# parser to get file name
parser <- ArgumentParser(description='stores file name')
parser$add_argument('--file', help='file name for i/o')
args <- parser$parse_args()
file_name <- args$file
print(file_name)
infile <- sprintf('/home/bmoginot/new_kraken/filtered_reads/%s_filtered.csv', file_name)
outfile <- sprintf('/home/bmoginot/new_kraken/filtered_reads/%s_curve.pdf', file_name)
print(c(infile, outfile))
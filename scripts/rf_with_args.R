library(vegan)
library(argparse)

# parser to get file name
parser <- ArgumentParser(description='stores file name')
parser$add_argument('--file', help='file name for i/o')
args <- parser$parse_args()
file_name <- args$file
infile <- sprintf('/home/bmoginot/new_kraken/filtered_reads/%s_filtered.csv', file_name)
outfile <- sprintf('/home/bmoginot/new_kraken/curves/%s_curve.pdf', file_name)

# importing the file and parsing the file correctly
# Replace the kraken_final name to the actual filename.
Data=read.table(infile, sep=",", row.names = 1, header=TRUE)
Data_t=as.data.frame(t(Data))

#count the number of species
S <- specnumber(Data_t)
raremax <-min(rowSums(Data_t))

#Rarefaction of the samples
Srare <- rarefy(Data_t, raremax)

#plotting the rarefaction curves
plot(S, Srare, xlab = "Observed No. of Species", ylab = "Rarefied No. of Species")
abline(0, 1)
pdf(outfile)
rarecurve(Data_t, step =20, sample = raremax, col = "blue", cex = 0.4, )
dev.off()
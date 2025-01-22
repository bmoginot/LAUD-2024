# iterate through the k2om files and convert them to csv

for d in /home/bmoginot/new_kraken/k2om_output/*
do
  sed -e "s/\[//g;s/\]//g;s/'//g;s|\t|,|g" $d > $d.csv
done

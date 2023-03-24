# Example run

## Create blastdb using your own adapter+barcode sequence

The provided example uses adapter_barcode.fa, but for your situation, a different file will be used instead. You should know your own adapter+barcode sequence.

`cd adapter_barcode_db`

`makeblastdb -in adapter_barcode.fa -dbtype nucl`

## Run blast with your Pacbio seqences

You can use different parameters for running blast, but "-outfmt 6" is required.

`cd ../`

`blastn -db ./adapter_barcode_db/adapter_barcode.fa -query example.fasta -outfmt 6 > blast_res.txt`

## Run hiTrim.py

`python3 ../hiTrim.py -i example.fasta -b blast_res.txt -o trimmed_sequences.fasta`
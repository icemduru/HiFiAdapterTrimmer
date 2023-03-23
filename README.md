# HiFiAdapterTrimmer
Adapter+Barcode trimming from Pacbio HiFi reads

Althoug reads that created by PacBio Sequel II should be adapter+barcode free, we can still get reads that contain those. hiTrim.py is a python script that help you to trim those reads. To use this script you first need to blast your adapter+barcode sequences againts your Pacbio reads.

## Requirements
python3.6+

biopython==1.81

## How to run
So probably you first need to run blast similar to this:

`makeblastdb -dbtype nucl -in adapter_barcode.fa`

`blastn -db adapter_barcode.fa -query my_hifi_reads.fasta -outfmt 6 -mt_mode 1 -num_threads 64 > blast_res.txt`

After you get your blast results, you can use hiTrim.py.

`python3 hiTrim.py -i my_sequences.fasta -b blast_res.txt -o filtered.fasta`

## Warnings
If a blast hit length is larger than 50 and the hit is in the middle of the read. The read will be discarded. The list of discarded reads can be seen in discarded_reads.txt.



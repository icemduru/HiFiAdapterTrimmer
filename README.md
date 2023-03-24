# HiFiAdapterTrimmer
Adapter+Barcode trimming from Pacbio HiFi reads

Despite the fact that the PacBio Sequel II generates reads that are supposed to be free of adapters and barcodes, it is still possible to obtain reads that contain them. To address this issue, hiTrim.py, a Python script, can be used to trim these reads. To utilize this script, the adapter+barcode sequences must first be BLASTed against the PacBio reads.

## Requirements
python3.6+

biopython==1.81

You can install biopython using:

`pip install biopython`

## How to run
So probably you first need to run blast similar to this:

`makeblastdb -dbtype nucl -in adapter_barcode.fa`

`blastn -db adapter_barcode.fa -query my_hifi_reads.fasta -outfmt 6 -mt_mode 1 -num_threads 64 > blast_res.txt`

After you get your blast results, you can use hiTrim.py.

`python3 hiTrim.py -i my_sequences.fasta -b blast_res.txt -o filtered.fasta`

The adapter+barcode sequences will be trimmed by hiTrim.py if those sequences are at the beggining or at the end of the hifi read.

## Warnings
If a blast hit length is larger than 50 and the hit is in the middle of the read. The read will be discarded. The list of discarded reads can be seen in discarded_reads.txt.



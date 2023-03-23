from Bio import SeqIO
import sys
import argparse

parser = argparse.ArgumentParser(description='Hifi Adapter trimming based on blast results', usage='\n python3 hiTrim.py -i [input hifi sequences] -b [blast result file] -o [output file name] \n \n example: python3 hiTrim.py -i my_sequences.fasta -b blast_res.txt -o filtered.fasta \n \n')
parser.add_argument('-b', dest='blastfile', required=True, help="the blast result file that you created using adapter+barcode sequence and with -outfmt 6")
parser.add_argument('-i', dest='input', required=True, help="input sequences .fasta, .fa")
parser.add_argument('-o', dest='output', required=True, help="output file name, for example: myfiltered_sequences.fasta")
args = parser.parse_args()

file1 = open(args.output, 'w')
file2 = open("discarded_reads.txt", 'w')
hits = dict()

for line in open(args.blastfile):
	line=line.strip()
	s_line=line.split('\t')
	#hit_start,hit_end,adapt_start_adapt_end,hit_len
	hits[s_line[0]] = [s_line[6],s_line[7],s_line[8],s_line[9],s_line[3]]

#print(hits)
print("filtering is started, output will be written in "+str(args.output)+" -- Reads that adapter found in the middle of the read will be removed, the list of removed ones can be seen in the file discarded_reads.txt")
with open(args.input) as handle:
	for record in SeqIO.parse(handle, "fasta"):
		if record.id in hits.keys():
			len_of_read = len(record.seq)
			start_of_hit = int(hits[record.id][0])
			end_of_hit = int(hits[record.id][1])
			if start_of_hit > 200 and end_of_hit > (len_of_read-200):
				file1.write('>'+str(record.id)+'\n')
				file1.write(str(record.seq[0:start_of_hit])+'\n')
			elif end_of_hit < 200 :
				file1.write('>'+str(record.id)+'\n')
				file1.write(str(record.seq[end_of_hit:])+'\n')
			elif int(hits[record.id][4]) < 51:
				file1.write('>'+str(record.id)+'\n')
				file1.write(str(record.seq)+'\n')
			else:
				file2.write("adapter is in the middle of the read of "+str(record.id)+". Read length is: "+str(len_of_read)+". Adapter is "+str(hits[record.id][4])+" bp long and position in the read is "+str(start_of_hit)+' '+str(end_of_hit)+". This reads won't be written in the output"+'\n')
		else:
			file1.write('>'+str(record.id)+'\n')
			file1.write(str(record.seq)+'\n')

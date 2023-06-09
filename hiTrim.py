from Bio import SeqIO
import sys
import argparse
from Bio.SeqIO.QualityIO import FastqGeneralIterator

parser = argparse.ArgumentParser(description='Hifi Adapter trimming based on blast results', usage='\n python3 hiTrim.py -i [input hifi sequences] -b [blast result file] -o [output file name] \n \n example: python3 hiTrim.py -i my_sequences.fasta -b blast_res.txt -o filtered.fasta \n \n')
parser.add_argument('-b', dest='blastfile', required=True, help="the blast result file that you created using adapter+barcode sequence and with -outfmt 6")
parser.add_argument('-i', dest='input', required=True, help="input sequences .fasta, .fa")
parser.add_argument('-o', dest='output', required=True, help="output file name, for example: myfiltered_sequences.fasta")
parser.add_argument('-l', dest='length', nargs='?', const=51, default=51, type=int, help="The length of blast hit to remove reads that adapter found in the middle of the read")
args = parser.parse_args()

input_format = ""
if args.input.split('.')[-1] == "fasta" or args.input.split('.')[-1] == "fa" or args.input.split('.')[-1] == "fna":
	input_format = "fasta"
elif args.input.split('.')[-1] == "fastq" or args.input.split('.')[-1] == "fq":
	input_format = "fastq"
else:
	sys.exit('Please use fasta, fa, fna, fastq, or fq formatted input')


file1 = open(args.output, 'w')
file2 = open('discarded_reads.txt', 'w')
file3 = open('hiTrim_logs.txt', 'w')
hits = dict()
remove_because_of_multiple_hit = []

for line in open(args.blastfile):
	line=line.strip()
	s_line=line.split('\t')
	if s_line[0] in hits.keys():
		remove_because_of_multiple_hit.append(s_line[0])
		hits.pop(s_line[0])
	else:
		#hit_start,hit_end,adapt_start_adapt_end,hit_len
		hits[s_line[0]] = [s_line[6],s_line[7],s_line[8],s_line[9],s_line[3]]

#print(hits)
print("filtering is started, output will be written in "+str(args.output)+" -- Reads that adapter found in the middle of the read will be removed, the list of removed ones can be seen in the file discarded_reads.txt")

if input_format == "fasta":

	with open(args.input) as handle:
		for record in SeqIO.parse(handle, "fasta"):
			if record.id in hits.keys():
				len_of_read = len(record.seq)
				start_of_hit = int(hits[record.id][0])
				end_of_hit = int(hits[record.id][1])
				if start_of_hit > 200 and end_of_hit > (len_of_read-200):
					file1.write('>'+str(record.id)+'\n')
					file1.write(str(record.seq[0:start_of_hit])+'\n')
					file3.write("Read trimmed: Position of the read written in the output "+str(record.id)+" 0 "+str(start_of_hit)+'\n')
				elif end_of_hit < 200 :
					file1.write('>'+str(record.id)+'\n')
					file1.write(str(record.seq[end_of_hit:])+'\n')
					file3.write("Read trimmed: Position of the read written in the output "+str(record.id)+" "+str(end_of_hit)+" "+str(len(record.seq))+'\n')
				elif int(hits[record.id][4]) < args.length:
					file1.write('>'+str(record.id)+'\n')
					file1.write(str(record.seq)+'\n')
				else:
					file2.write("adapter is in the middle of the read of "+str(record.id)+". Read length is: "+str(len_of_read)+". Adapter is "+str(hits[record.id][4])+" bp long and position in the read is "+str(start_of_hit)+' '+str(end_of_hit)+". This reads won't be written in the output"+'\n')
			else:
				if record.id in remove_because_of_multiple_hit:
					continue
				else:
					file1.write('>'+str(record.id)+'\n')
					file1.write(str(record.seq)+'\n')

	for line in remove_because_of_multiple_hit:
		line=line.strip()
		file2.write('The read '+line+' is discarted because of double blast hit.'+'\n')

elif input_format == "fastq":

	with open(args.input) as handle:
		for record_id,seq,qual in FastqGeneralIterator(handle):
			if record_id in hits.keys():
				len_of_read = len(seq)
				start_of_hit = int(hits[record_id][0])
				end_of_hit = int(hits[record_id][1])
				if start_of_hit > 200 and end_of_hit > (len_of_read-200):
					file1.write('@'+str(record_id)+'\n')
					file1.write(str(seq[0:start_of_hit])+'\n')
					file1.write("+"+'\n')
					file1.write(str(qual[0:start_of_hit])+'\n')
					file3.write("Read trimmed: Position of the read written in the output "+str(record_id)+" 0 "+str(start_of_hit)+'\n')
				elif end_of_hit < 200 :
					file1.write('@'+str(record_id)+'\n')
					file1.write(str(seq[end_of_hit:])+'\n')
					file1.write("+"+'\n')
					file1.write(str(qual[end_of_hit:])+'\n')
					file3.write("Read trimmed: Position of the read written in the output "+str(record_id)+" "+str(end_of_hit)+" "+str(len(seq))+'\n')
				elif int(hits[record_id][4]) < args.length:
					file1.write('@'+str(record_id)+'\n')
					file1.write(str(seq)+'\n')
					file1.write("+"+'\n')
					file1.write(str(qual)+'\n')
				else:
					file2.write("adapter is in the middle of the read of "+str(record_id)+". Read length is: "+str(len_of_read)+". Adapter is "+str(hits[record_id][4])+" bp long and position in the read is "+str(start_of_hit)+' '+str(end_of_hit)+". This reads won't be written in the output"+'\n')
			else:
				if record_id in remove_because_of_multiple_hit:
					continue
				else:
					file1.write('@'+str(record_id)+'\n')
					file1.write(str(seq)+'\n')
					file1.write("+"+'\n')
					file1.write(str(qual)+'\n')

	for line in remove_because_of_multiple_hit:
		line=line.strip()
		file2.write('The read '+line+' is discarted because of double blast hit.'+'\n')




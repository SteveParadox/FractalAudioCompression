#!usr/bin/python
# @author Mayank Gupta
import os
import sys
import wave
import binascii
from collections import OrderedDict


class Block:#class for frame

	def __init__(self, frame):
		self.data=0
		self.size=0
		for i in frame:
			self.size = self.size + 1
			self.data=self.data*256  + int(ord(i))#input file may contain 1 or 2 bytes per frame
		self.voiced=0

	def voiced_or_not(self,last,curr,next):#calculates wether a block is voiced or unvoiced
		if last != curr or next !=curr:
			self.voiced=1
		else:
			self.voiced=0



class IFSBlock:#block for IFS - Iterated Function System
	def __init__(self,scale,position,mean,sym):
		self.scale = scale
		self.position = position
		self.mean = mean
		self.sym = sym

	def ifs_set(self,scale,position,mean,sym):#modify value of ifs
		self.scale = scale
		self.position = position
		self.mean = mean
		self.sym = sym



def range_pool(frames,num,range_size,rp):#creates range pool
	for i in range(num/range_size):
		rp.append([])
		for j in range(range_size):
			rp[i].append(frames[(i-1)*range_size + j].data * frames[(i-1)*range_size + j].voiced)



def domain_pool(frames,num,dp,tile_size):#creates domain pool
	domain_size=tile_size/2-1
	for i in range(num/tile_size - 1):
		dp.append([])
		for pd in range(domain_size):
			pr=pd+pd
			dp[i].append((frames[(i-1)*tile_size + pr].data * frames[(i-1)*tile_size + pr].voiced + frames[(i-1)*tile_size + pr+1].data * frames[(i-1)*tile_size + pr+1].voiced)/2)



def compute_average_range(r):#computes average range
	rb=0.0
	m=float(len(r))
	for x in r:
		rb = rb + x/m
	return int(rb)



def compute_average_domain(d):#computes average domain
	db=0.0
	m=float(len(d))
	for x in d:
		db = db + x/m
	return int(db)



def compute_variance_range(r,rb):#computes variance for range
	sr2=0.0
	m=float(len(r))
	for x in r:
		sr2 = sr2 + (x*x)/m
	return int(sr2)



def compute_variance_domain(d,db):#computes variance for domain
	sd2=0.0
	m=float(len(d))
	for x in d:
		sd2 = sd2 + (x*x)/m
	sd2 = sd2 - (db*db)
	return int(sd2)



def compute_scale(db,rb,sd2,m,srd):#computes scale
	if sd2 <= 0:
		return 0
	s = srd/float(m) - db*rb
	return int(s)



def compute_chi(sr2,s,sd2,db,rb,m,srd):#computes error (chi)
	chi2=0.0
	chi2 = sr2 + s*(s*sd2 + 2*db*rb - 2*srd/float(m))
	chi = chi2**(1/2.0)
	return int(chi)



def main():#main function
	try:
		inputfile = sys.argv[1]#input file
		tile_size = int(sys.argv[2])#tile size
	except:
		print 'python [scriptfile] [inputfile] tile_size'
		return
		
	ip = wave.open(inputfile, 'r')#open input file
	op = open(inputfile.split('.')[0] + '.wavc', 'w')#open output file
	op.write('This wave file has been compressed using fractal compression\n')
	op.write('Number of channels = ' + str(ip.getnchannels()) + "\n")
	op.write('Sample width = ' + str(ip.getsampwidth()) + "\n")
	op.write('Number of frames = ' + str(ip.getnframes()) + "\n")
	op.write('Frame rate = ' + str(ip.getframerate()) + "\n")
	op.write('Number of channels = ' + str(ip.getnchannels()) + "\n")

	width=ip.getsampwidth()
	num=ip.getnframes()

	range_size = tile_size/16
	tile_to_range = tile_size/(2*range_size)
	jump_step = tile_to_range/8

	frames=[]
	for i in range(num):
		frame=Block(ip.readframes(1))#read frames from input file and put them in a list
		frames.append(frame)

	last=frames[0]
	curr=frames[0]
	for next in frames:
		curr.voiced_or_not(last,curr,next)#use adjacent frames to decide voiced or unvoiced
		last=curr
		curr=next

	rp=[]
	dp=[]
	range_pool(frames,num,range_size,rp)
	domain_pool(frames,num,dp,tile_size)

	db=[]
	sd2=[]
	for d in range(len(dp)):
		db.append(compute_average_domain(dp[d]))
		sd2.append(compute_variance_domain(dp[d],db[d]))

	ifs_list = []#to store all ifs
	domain_used = OrderedDict()
	for r in range(len(rp)):
		rb = compute_average_range(rp[r])
		sr2 = compute_variance_range(rp[r],rb)
		minerror= 9E+19#define minerror
		ifs = IFSBlock(0,0,0,0)
		for d in range(len(dp)):
			for pd in range(tile_to_range/jump_step - 1):
				srd=[]
				srd.append(0)
				srd.append(0)
				for i in range(0,range_size):
					srd[0]=srd[0]+dp[d][i*tile_to_range+pd*jump_step]*rp[r][i]#compute summation of r[i]*d[i]
					srd[1]=srd[1]+dp[d][i*tile_to_range+pd*jump_step]*rp[r][range_size-1-i]#compute summation of r[i]*d[n - i]
				for j in range(len(srd)):#to check if original or its mirror is better fit
					s = compute_scale(db[d],rb,sd2[d], len(rp[r]), srd[j])
					chi = compute_chi(sr2, s, sd2[d], db[d], rb, len(rp[r]), srd[j])
					if minerror > chi:
						minerror = chi#calculate minimum error
						ifs.ifs_set(s,d,rb,j)
		domain_used[ifs.position] = True#keep a list of domains used
		ifs_list.append(ifs)

	domain_used=sorted(domain_used)
	op.write('No. of Domains= ' + str(len(domain_used)) + '\n')
	for d in domain_used:
		op.write('Domain no. = ' + str(d) + '\n')
		op.write('Domain = ')
		for i in dp[d]:
			if(frame.size > 1):#input file may contain 1 or 2 bytes per frame
				op.write(binascii.b2a_hex(chr(i/256)))
			op.write(binascii.b2a_hex(chr(i%256))+ ' ')#convert ascii to string to hex and store required domain in output file
		op.write('\n')

	op.write('Scale\tPosition\tMean\tSym\n')
	for ifs in ifs_list:
		op.write(str(ifs.scale)  + "\t\t" + str(ifs.position) + "\t\t\t"  + str(ifs.mean) + "\t\t" + str(ifs.sym) + "\n")#store ifs in output file

	print 'Compression ratio = ' + str( 2.0 * num / (len(domain_used) * tile_size))#calculate compression ratio
	print 'Output file = ' + inputfile.split('.')[0] + '.wavc\n'
	ip.close()
	op.close()

if  __name__ =='__main__':main()
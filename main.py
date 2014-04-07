#!usr/bin/python
# @author Mayank Gupta
import os,sys,wave,struct


class Block:

	def __init__(self, frame):
		# print "len"
		# print len(frame)
		# print frame
		# self.data = struct.unpack("BH", frame)
		self.data=int(ord(frame))
		self.voiced=0

	def voiced_or_not(self,last,curr,next):
		if last != curr or next !=curr:
			self.voiced=1
		else:
			self.voiced=0


def range_pool(frames,num,range_size,rp):
	for i in range(num/range_size):
		rp.append([])
		for j in range(range_size):
			rp[i].append(frames[(i-1)*range_size + j].data * frames[(i-1)*range_size + j].voiced)

def domain_pool(frames,num,dp,tile_size):
	domain_size=tile_size/2-1
	for i in range(num/tile_size - 1):
		dp.append([])
		for pd in range(domain_size):
			pr=pd+pd
			dp[i].append((frames[(i-1)*tile_size + pr].data * frames[(i-1)*tile_size + pr].voiced + frames[(i-1)*tile_size + pr+1].data * frames[(i-1)*tile_size + pr+1].voiced)/2)

def compute_average_range(r):
	rb=0.0
	m=float(len(r))
	for x in r:
		rb = rb + x/m
	# print rb
	return int(rb)

def compute_average_domain(d):
	db=0.0
	m=float(len(d))
	for x in d:
		db = db + x/m
	# print db
	return int(db)

def compute_variance_range(r,rb):
	sr2=0.0
	m=float(len(r))
	for x in r:
		sr2 = sr2 + (x*x)/m
	# print sr2
	return int(sr2)

def compute_variance_domain(d,db):
	sd2=0.0
	m=float(len(d))
	for x in d:
		sd2 = sd2 + (x*x)/m
	sd2 = sd2 - (db*db)
	# print sd2
	return int(sd2)

def compute_scale(db,rb,sd2,m,srd):
	if sd2 <= 0:
		return 0
	s = srd/float(m) - db*rb
	return int(s)

def compute_chi(sr2,s,sd2,db,rb,m,srd):
	chi2=0.0
	chi2 = sr2 + s*(s*sd2 + 2*db*rb - 2*srd/float(m))
	chi = chi2**(1/2.0)
	return int(chi)



class IFSBlock:
	def __init__(self,scale,position,mean,sym):
		self.scale = scale
		self.position = position
		self.mean = mean
		self.sym = sym

	def ifs_set(self,scale,position,mean,sym):
		self.scale = scale
		self.position = position
		self.mean = mean
		self.sym = sym

def main():
	try:
		inputfile = sys.argv[1]
		outputfile = sys.argv[2]
		tile_size = int(sys.argv[3])
	except:
		inputfile='input.wav'
		outputfile='output.wav'
		tile_size = 512
		
	ip = wave.open(inputfile, 'r')
	op = wave.open(outputfile, 'w')
	op.setnchannels(ip.getnchannels())
	op.setsampwidth(ip.getsampwidth())
	op.setframerate(ip.getframerate())
	op.setnframes(ip.getnframes())
	op2 = open('o.txt','w')
	
	width=ip.getsampwidth()
	num=ip.getnframes()
	range_size = tile_size/8
	tile_to_range = tile_size/(2*range_size)
	jump_step = tile_to_range/4
	# print width
	# print num
	# print ip.getframerate()

	frames=[]
	for i in range(num):
		# op.writeframes(ip.readframes(1))
		frame=Block(ip.readframes(1))
		# print frame.data
		frames.append(frame)

	last=frames[0]
	curr=frames[0]
	for next in frames:
		curr.voiced_or_not(last,curr,next)
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
		# print str(db[d]) + " " + str(sd2[d])

	ifs_list = []
	for r in range(len(rp)):
		rb = compute_average_range(rp[r])
		sr2 = compute_variance_range(rp[r],rb)
		minerror= 9E+19
		ifs = IFSBlock(0,0,0,0)
		for d in range(len(dp)):
			for pd in range(tile_to_range/jump_step - 1):
				srd=[]
				srd.append(0)
				srd.append(0)
				for i in range(0,range_size):
					srd[0]=srd[0]+dp[d][i*tile_to_range+pd*jump_step]*rp[r][i]
					srd[1]=srd[1]+dp[d][i*tile_to_range+pd*jump_step]*rp[r][range_size-1-i]
				for j in range(len(srd)):
					s = compute_scale(db[d],rb,sd2[d], len(rp[r]), srd[j])
					chi = compute_chi(sr2, s, sd2[d], db[d], rb, len(rp[r]), srd[j])
					if minerror > chi:
						minerror = chi
						ifs.ifs_set(s,d,rb,j)
		ifs_list.append(ifs)


	print len(rp)
	print len(ifs_list)
	print len(dp)
	for ifs in ifs_list:
		# print ifs.scale, ifs.position, ifs.mean, ifs.sym
		op2.write(str(ifs.scale)  + " " + str(ifs.position) + " "  + str(ifs.mean) + " " + str(ifs.sym) + "\n")
	# for frame in frames:
	# print frame.data, frame.voiced
	
	ip.close()
	op.close()
	op2.close()

if  __name__ =='__main__':main()
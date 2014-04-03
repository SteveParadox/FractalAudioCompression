#!usr/bin/python
# @author Mayank Gupta
import os,sys,wave


class Block:

	def __init__(self, frame):
		self.data = frame

	def voiced_or_not(self,last,curr,next):
		if last != curr or next !=curr:
			self.voiced=1
		else:
			self.voiced=0


def range_pool(frames,num,size,r):
	for i in range(1,num):
		r.append([])
		for j in range(1,size):
			if frames[(i-1)*size+j].voiced == 1:
				r[i].append(frames[(i-1)*size+j].data)

def domain_pool(frames,num,d):
	size=num/2-1
	for pd in range(0,size):
		pr=pd+pd
		d.append(frames[pr].data)

def compute_average_range(r):
	return rb

def compute_average_domain(d):
	return db

def compute_variance_range(r,rb):
	return sr2

def compute_variance_domain(d,db):
	return sd2



def main():
	try:
		inputfile = sys.argv[1]
		outputfile = sys.argv[2]
	except:
		inputfile='input.wav'
		outputfile='output.wav'

	# with open(inputfile, "rb") as ip:
	# 	chunkid = ip.read(4)
	# 	chunksize = ip.read(4)
	# 	format = ip.read(4)
	# 	subchunk1id = ip.read(4)
	# 	Subchunk1Size = ip.read(4)
	# 	AudioFormat = ip.read(2)
	# 	NumChannels = ip.read(2)
	# 	SampleRate = ip.read(4)
	# 	ByteRate = ip.read(4)
	# 	BlockAlign = ip.read(2)
	# 	BitsperSample = ip.read(2)
	# 	ExtraFormat = ip.read(2)
	# 	FactChunkID = ip.read(4)
	# 	FactChunkSize = ip.read(4)
	# 	DependentData = ip.read(4)
	# 	Subchunk2ID = ip.read(4)
	# 	Subchunk2Size = ip.read(4)

	# 	print 'chunkid = ' + chunkid
	# 	print 'chunksize = ' + chunksize
	# 	print 'format = ' + format
	# 	print 'subchunk1id = ' + subchunk1id
	# 	print 'Subchunk1Size = ' + Subchunk1Size
	# 	print 'AudioFormat = ' + AudioFormat
	# 	print 'NumChannels = ' + NumChannels
	# 	print 'SampleRate = ' + SampleRate
	# 	print 'ByteRate = ' + ByteRate
	# 	print 'BlockAlign = ' + BlockAlign
	# 	print 'BitsperSample = ' + BitsperSample
	# 	print 'ExtraFormat = ' + ExtraFormat
	# 	print 'FactChunkID = ' + FactChunkID
	# 	print 'FactChunkSize = ' + FactChunkSize
	# 	print 'DependentData = ' + DependentData
	# 	print 'Subchunk2ID = ' + Subchunk2ID
	# 	print 'Subchunk2Size = ' + Subchunk2Size
		
	ip = wave.open(inputfile, 'r')
	op = wave.open(outputfile, 'w')
	op.setnchannels(ip.getnchannels())
	op.setsampwidth(ip.getsampwidth())
	op.setframerate(ip.getframerate())
	op.setnframes(ip.getnframes())
	
	width=ip.getsampwidth()
	num=ip.getnframes()

	print width
	print num
	print ip.getframerate()

	frames=[]
	for i in range(num):
		# op.writeframes(ip.readframes(1))
		frame=Block(ip.readframes(1))
		# print frame.data , frame.voiced
		frames.append(frame)

	last=frames[0]
	curr=frames[0]
	for next in frames:
		curr.voiced_or_not(last,curr,next)
		last=curr
		curr=next

	r=[]
	d=[]
	range_pool(frames,num,1,r)
	domain_pool(frames,num,d)

	for frame in frames:
		print frame.data, frame.voiced
	ip.close()
	op.close()
		






if  __name__ =='__main__':main()


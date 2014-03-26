#!usr/bin/python
# @author Mayank Gupta
import os,sys,wave


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

	for i in range(ip.getnframes()):
		op.writeframes(ip.readframes(1))
	
	ip.close()
	op.close()
		
		
		
		
		
		
		
#    	while byte:
	#       	byte = ip.read(1)

if  __name__ =='__main__':main()


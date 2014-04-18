FractalAudioCompression
=======================

This project aims to implement Fractal Audio Compression in python for .wav files.
A .wav file specifying tile size is passed as argument to the program. Based on bits per sample, data is extracted from this file. Tile size represents the size of domain block i.e. the size of each partition which will represent the compressed audio file.
The data is read as frames from the audio file and categorized as voiced or unvoiced based on whether there is a sign change among adjacent frames or not, respectively. This is followed by dividing the data into non-overlapping blocks of tile size for domain pool and range size (= tile size / 16 in current project) for range pool. Domain pool is constructed by down-sampling the data (2 in current project). Range pool is created for each block.
For each range block, a domain block is identified which is more similar to former than all other available domain blocks. This is done by computing scale and error values using average and variances. Following formulas show how to calculate the required values. 
Based on parameters and domain block for each range block, IFS (Iterated Function System) parameters are generated. The IFS parameters along with domain ranges used, are stored in a file which represents the compressed version of the .wav file and is given extension .wavc in current project.



To view demonstration -

python [scriptname] [inputfile] tile_size
where
	scriptname = name of .py file which contains code for fractal compression
inputfile = a .wave file which needs to be compressed
tile_size = defines the size of tile which will be used to break the audio into domains
Output is stored in [inputfile].wavc




# /usr/bin/python 
import sys,re,getopt

def usage():
	print "\n\t AnalyseSiminst.py -i <siminst-file> -s <systemID of cache> \n\t Optional inputs: -l <Number of cache levels:default=3> -hy <0: Standard memory 1: Hybrid memory> -o <Output-file> "
	sys.exit()
def WhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output
	
def main(argv):
        SiminstFile=''
        debug=0
        verbose=False
        SysID=''
        NumCacheLevels=''
        HybridMemory=''
        OutFileName=''
        try:
           opts, args = getopt.getopt(sys.argv[1:],"i:s:l:y:o:h:v",["input","sysid","levels","hybrid","output","help","verbose"])
        except getopt.GetoptError:
                #print str(err) # will print something like "option -a not recognized"
           usage()
           sys.exit(2)
        #verbose=False   
        for opt, arg in opts:
           if opt == '-h':
              usage()
              sys.exit()
           elif opt in ("-i", "--input"):
              SiminstFile=arg
              print "\n\t Input file is "+str(SiminstFile)
           elif opt in ("-s", "--sysid"):
              StrSysID=WhiteSpace(arg)
              SysID=int(StrSysID)
              print "\n\t Sysid is "+str(SysID)
           elif opt in ("-l", "--levels"):
           	StrNumCacheLevels=WhiteSpace(arg)
           	NumCacheLevels=int(StrNumCacheLevels)
           	print "\n\t Number of Cache Levels: "+str(NumCacheLevels)
           elif opt in ("-y", "--hybrid"):
           	StrHybridMemory=WhiteSpace(arg)
           	HybridMemory=int(StrHybridMemory)
           	print "\n\t HybridMemory: "+str(HybridMemory)
           elif opt in ("-o","--output"):
           	OutFileName=WhiteSpace(arg)
           	print "\n\t Out file is "+str(OutFileName)
           elif opt in ("-v","--verbose"):
           	verbose=False
	   else:  
		usage()
		

	if( (SiminstFile=='') or (SysID=='') ):
		usage()
	if(NumCacheLevels==''):
		NumCacheLevels=3
		print "\n\t Using default number of cache levels: "+str(NumCacheLevels)
	if(HybridMemory==''):
		HybridMemory=0
		print "\n\t Assuming the memory is not hybrid \n" ;
	if(OutFileName!=''):
		OutStream=open(OutFileName,'w')
	else:
		OutStream=sys.stdout
		
	Inp=open(SiminstFile)
	Input=Inp.readlines()
	NumBlks=0
	# If this script is used for more than one task, can use the following nested loop as a method.
	NumCacheLevels+=HybridMemory
	InputLen=len(Input)
	OutStream.write("\n\t Format: <Blk-ID> <Hits> <Misses> <Loads> <Stores> \n");
	for LineNum in range(InputLen):
		CurrLine=Input[LineNum]
		BlkLine=re.match('\s*BLK\s*\d+\s*0x(.*)\s*.*',CurrLine)
		if BlkLine:
			BlockID=re.split('\t',BlkLine.group(1))
			#print "\n\t Is this the BlockID: "+str(BlockID[0])
			NumBlks+=1
			MaxLine=LineNum+1+1 #Just need 1st level info now!
			for AdjLineNum in range(LineNum+1,MaxLine):
				CurrLine=Input[AdjLineNum]
				#print "\n\t Investigating line "+str(CurrLine)
				CacheStats=re.split('\t',CurrLine)
				if CacheStats:
					SysIDIdx=1
					LocalSysID=WhiteSpace(CacheStats[SysIDIdx])
					#print "\n\t LocalSysID: "+str(LocalSysID)
					if( SysID==int(LocalSysID)):
						#print "\n\t Found SysID "+str(SysID)+" related stats in line "+str(AdjLineNum)
						if(len(CacheStats)<(SysIDIdx+6)):
							print "\n\t Error: The CacheStat line is expected to have "+str(SysIDIdx+6)+" fields while the specified cache line only has "+str(len(CacheStats))+" number of fields "
							sys.exit()
						OutStream.write("\t "+str(BlockID[0])+"\t"+str(CacheStats[SysIDIdx+2])+"\t"+CacheStats[SysIDIdx+3]+"\t"+str(CacheStats[SysIDIdx+4])+"\t"+str(CacheStats[SysIDIdx+5]))
	
	print "\n\t NumBlks: "+str(NumBlks)		

if __name__=="__main__":
	main(sys.argv[1:])

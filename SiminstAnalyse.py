# /usr/bin/python 
import sys,re,getopt
import ExtractHitRatesM

debug=0

def usage():
	print "\n\t AnalyseSiminst.py -i <siminst-file> -s <systemID of cache> \n\t Optional inputs: -p <Percent of Other Controlling factor:default=100>-r <Ratio coefficient:default=1> -l <Number of cache levels:default=3> -H <0: Standard memory 1: Hybrid memory> -o <Output-file> "
	sys.exit()
def WhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output

def hex2dec(Hex):
	HexExtracted=re.match('\s*0x(.*)',Hex)	
	if HexExtracted:
		Dec=int(HexExtracted.group(1),16)
		return Dec
	else:
		print "\n\t ERROR: Unable to extract hexadecimal number! \n\n"
		sys.exit(0)
		
def main(argv):
        SiminstFile=''
        #debug=0
        verbose=False
        SysID=''
        NumCacheLevels=''
        HybridMemory=''
        OutFileName=''
        RatioCoefficient=''
        PercentControl=''
        try:
           opts, args = getopt.getopt(sys.argv[1:],"i:s:r:p:l:H:o:h:v",["input","sysid","ratio","percent","levels","hybrid","output","help","verbose"])
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
           elif opt in ("-H", "--hybrid"):
           	StrHybridMemory=WhiteSpace(arg)
           	HybridMemory=int(StrHybridMemory)
           	print "\n\t HybridMemory: "+str(HybridMemory)
           elif opt in ("-p", "--percent"):
           	PercentControlStr=WhiteSpace(arg)
           	PercentControl=float(PercentControlStr)
           	print "\n\t PercentControl: "+str(PercentControl)  
           elif opt in ("-r", "--ratio"):
           	RatioCoefficientStr=WhiteSpace(arg)
           	RatioCoefficient=float(RatioCoefficientStr)
           	print "\n\t RatioCoefficient: "+str(RatioCoefficient)             	         	
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
	if(RatioCoefficient==''):
		RatioCoefficient=1.0
		print "\n\t Assuming the ratio requested is "+str(RatioCoefficient)+"\n"
	if(PercentControl==''):
		PercentControl=0.0
		print "\n\t Assuming the percent control requested is "+str(PercentControl)+"\n"
	if(OutFileName!=''):
		OutStream=open(OutFileName,'w')
	else:
		OutStream=sys.stdout
		
	Inp=open(SiminstFile)
	Input=Inp.readlines()
	Inp.close()
	NumBlks=0
	# If this script is used for more than one task, can use the following nested loop as a method.
	NumCacheLevels+=HybridMemory
	InputLen=len(Input)
	#OutStream.write("\n\t Format:-- <Blk-ID> <Hits> <Misses> <Loads> <Stores> \n");
	OutStream.write("\n\t Format: -- <Blk-ID> <StoresPercent> <LoadsPercent> <StoresPercentinBB> <LoadsPercentinBB> <MemRefPercentofBB> <StartAddress> <EndAddress> \n");
	SysIDIdx=1
	HitsID=SysIDIdx+2
	MissID=SysIDIdx+3
	LoadID=SysIDIdx+4
	StoreID=SysIDIdx+5
	#RatioCoefficient=1.0
	SuitableBlks=0
	TotalSuitableMemRef=0.0
	TotalSuitableStoreRefPercent=0.0
	Steps=10
	PercentCap=50
	RefPercentHistogram={}
	Bins=int(PercentCap/Steps)
	RefPercentHistogram['Mem']={}
	RefPercentHistogram['Store']={}
	for CurrBin in range(Bins):
		RefPercentHistogram['Mem'][CurrBin]=float(0.0)
		RefPercentHistogram['Store'][CurrBin]=float(0.0)
		
		#print "\n\t Bin: "+str(CurrBin)+" MemRefPercent: "+str(RefPercentHistogram[CurrBin])
	
 	ReqStats=ExtractHitRatesM.main(SiminstFile,SysID)
 	TotalAccesses=int(ReqStats['Loads'][0][1])
	OutStream.write("\n\t Accesses: "+str(TotalAccesses)+" Hits: "+str(float(float(ReqStats['Hits'][0][0])/float(ReqStats['Hits'][0][1])))+" Loads: "+str(float( float(ReqStats['Loads'][0][0])/float(ReqStats['Loads'][0][1])))+"\n\n")
	print("\n\t Accesses: "+str(TotalAccesses)+" Hits: "+str(float(float(ReqStats['Hits'][0][0])/float(ReqStats['Hits'][0][1])))+" Loads: "+str(float( float(ReqStats['Loads'][0][0])/float(ReqStats['Loads'][0][1]))))
	#print "\n\t TotalAccesses: "+str(TotalAccesses)
	for LineNum in range(InputLen):
		CurrLine=Input[LineNum]
		BlkLine=re.match('\s*BLK\s*\d+\s*0x(.*)\s*.*',CurrLine)
		if BlkLine:
			BlockID=re.split('\t',BlkLine.group(1))
			BlockAddressStartIdx=5
			BlockAddressEndIdx=6
			#for BlockStats in BlockID:
			#print "\n\t Is this the BlockID: "+str(BlockID[0])
			NumBlks+=1
			MaxLine=LineNum+1+1 #Just need 1st level info now!
			for AdjLineNum in range(LineNum+1,MaxLine):
				CurrLine=Input[AdjLineNum]
				#print "\n\t Investigating line "+str(CurrLine)
				CacheStats=re.split('\t',CurrLine)
				if CacheStats:
					#SysIDIdx=1
					LocalSysID=WhiteSpace(CacheStats[SysIDIdx])
					#print "\n\t LocalSysID: "+str(LocalSysID)
					if( SysID==int(LocalSysID)):
						#print "\n\t Found SysID "+str(SysID)+" related stats in line "+str(AdjLineNum)
						if(len(CacheStats)<(SysIDIdx+6)):
							print "\n\t Error: The CacheStat line is expected to have "+str(SysIDIdx+6)+" fields while the specified cache line only has "+str(len(CacheStats))+" number of fields "
							sys.exit()
						Loads=int(CacheStats[LoadID]) 
						Stores=int(CacheStats[StoreID])
						
						if( ( Stores > -2)):#0000) and ( (RatioCoefficient  * Loads ) < ( Stores ) ) ):
						#if( ( (RatioCoefficient  * Loads ) < ( Stores ) ) ):
						#if(int(CacheStats[StoreID]) > 100000):
							#OutStream.write("\t "+str(BlockID[0])+"\t"+str(CacheStats[HitsID])+"\t"+CacheStats[MissID]+"\t"+str(CacheStats[LoadID])+"\t"+str(CacheStats[StoreID]))
							#OutStream.write("\t "+str(BlockID[0])+"\t"+" Start: "+str(BlockID[BlockAddressStartIdx])+" End: "+str(BlockID[BlockAddressEndIdx]))
							MemRefPercent=float( 100*float(Loads+Stores) / TotalAccesses) 
							StoresPercentBB=0.0
							LoadsPercentBB=0.0
							#TotalSuitableMemRef+=Loads+Stores
							if(Loads):
								StoresPercentBB= float(100*float(Stores)/ (Stores+Loads))
								LoadsPercentBB=100-StoresPercentBB;
							else:
								StoresPercentBB=100.0
							#if( (StoresPercentBB < PercentCap) and (MemRefPercent > 0.5 ) ):
							if((MemRefPercent >= RatioCoefficient ) ):
								StoresPercent=(float(100*Stores)/TotalAccesses)
								LoadsPercent=(float(100*Loads)/TotalAccesses)
								if(StoresPercentBB>=PercentControl):
									RefPercentHistogram['Mem'][int(MemRefPercent/Steps)]+=MemRefPercent
									StoresAsAccessesPercent=(float( 100*Stores)/TotalAccesses)								
									RefPercentHistogram['Store'][int(StoresPercent/Steps)]+=StoresPercent
									SuitableBlks+=1
									TotalSuitableMemRef+=(Loads+Stores) #MemRefPercent
									TotalSuitableStoreRefPercent+=Stores
									BlockID[BlockAddressStartIdx]=hex2dec(BlockID[BlockAddressStartIdx])
									BlockID[BlockAddressEndIdx]=hex2dec(BlockID[BlockAddressEndIdx])
									OutStream.write("\n\t "+str(BlockID[0])+"\t"+"%.4f"%StoresPercent+"\t"+"%.4f"%LoadsPercent+"\t"+"%.3f"%StoresPercentBB+"\t"+"%.3f"%LoadsPercentBB+"\t"+"%.3f"%MemRefPercent+"\t"+str(BlockID[BlockAddressStartIdx])+"\t\t"+str(BlockID[BlockAddressEndIdx]))
									#OutStream.write("\n\t"+str(BlockID[BlockAddressStartIdx])+"\t"+str(BlockID[BlockAddressEndIdx]))
	TotalSuitableStoreRefPercent=(float(100*TotalSuitableStoreRefPercent)/TotalAccesses)
	TotalSuitableMemRef=(float(100*TotalSuitableMemRef)/TotalAccesses)
	for CurrBin in RefPercentHistogram['Mem']:
		print "\n\t Percent: "+str(CurrBin*Steps)+" MemRefPercent: "+str(RefPercentHistogram['Mem'][CurrBin])+" StoresRefPercent "+str(RefPercentHistogram['Store'][CurrBin])
			
	if(TotalSuitableMemRef):
		OutStream.write("\n\n\t Found "+str(NumBlks)+" of which "+str(SuitableBlks)+" have Percent-cap of "+str(PercentControl)+" or ratio coefficent of "+str(RatioCoefficient)+"\t TotalSuitableMemRef: "+str(TotalSuitableMemRef) +"\t TotalSuitableStoreRefPercent: "+str(TotalSuitableStoreRefPercent))
		print("\n\n\t Found "+str(NumBlks)+" of which "+str(SuitableBlks)+" have Percent-cap of "+str(PercentControl)+" or ratio coefficent of "+str(RatioCoefficient)+"\t TotalSuitableMemRef: "+str(TotalSuitableMemRef)+"\t TotalSuitableStoreRefPercent: "+str(TotalSuitableStoreRefPercent ))
	else:
		OutStream.write("\n\n\t Found "+str(NumBlks)+" of which "+str(SuitableBlks)+" have Percent-cap of "+str(PercentControl) +" or ratio coefficent of "+str(RatioCoefficient)+"\t TotalSuitableStoreRefPercent: "+str(TotalSuitableStoreRefPercent))		
		print("\n\n\t Found "+str(NumBlks)+" of which "+str(SuitableBlks)+" have Percent-cap of "+str(PercentControl)+" or ratio coefficent of "+str(RatioCoefficient)+"\t TotalSuitableStoreRefPercent: "+str(TotalSuitableStoreRefPercent))		

	#print("\n\n\t Found "+str(NumBlks)+" of which "+str(SuitableBlks)+" have RatioCoefficient of "+str(RatioCoefficient) )		
	OutStream.write("\n\n\n")

if __name__=="__main__":
	main(sys.argv[1:])

# /usr/bin/python 
import sys,re,getopt

def usage():
	print "\n\t ExtractCacheStats.py -i <siminst-file> -c <cache-specification-file>"
	sys.exit()
	
def WhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output
#def TotalMemoryAccessTime(CacheStats,MemoryDelays):
#	for keys in CacheStats:

	
def ReadCacheSpecs(CacheSpecsInp):
	CacheSpecs={}
	LineNum=0
	CacheSpecs['SysID']=[]
	for CurrLine in CacheSpecsInp:
		LineNum+=1
		CheckComment=re.match('^\s*\#',CurrLine)
		if CheckComment:
			print "\n\t Line-num is comment "+str(LineNum)	
		else:
			CheckEmptyLine=re.match('^\s*$',CurrLine)
			if CheckEmptyLine:
				print "\n\t Line-num is empty "+str(LineNum)	
			else:
				SeperateColon=re.split(';',CurrLine)
				if(len(SeperateColon)!=5):
					print "\n\t Format error: expected 5 fields, which are seperated by 4 semicolons in line "+str(LineNum)
					sys.exit()	
				else:
					CurrSysID=WhiteSpace(SeperateColon[0])
					CacheSpecs['SysID'].append(CurrSysID)	
					NumCacheLevels=int(WhiteSpace(SeperateColon[1]))
					Hybrid=int(WhiteSpace(SeperateColon[2]))
					if(Hybrid):
						NumCacheLevels+=1	
					print "\n\t Curr Sys ID is: "+str(CurrSysID)+" NumCache: "+str(NumCacheLevels)+" Hybrid "+str(Hybrid) 			
					ResponseDelay=re.split('\),',SeperateColon[3])
					if( (len(ResponseDelay)) >= (NumCacheLevels+1)):
						print "\n\t Found "+str(len(ResponseDelay))+" tuples for memory-response-delay specs! "
						ExtractedLevels=0;
						CacheSpecs['SysID']=[]
						CurrLevelDict={}
						CurrLevel=0
						CurrLevelDict[CurrLevel]={}
						CurrLevelDict[CurrLevel]['Latency']=[]
						"""for CurrTuple in ResponseDelay:
							RemoveBraces=re.sub('\s*\(','',CurrTuple);
							if RemoveBraces:
								CurrTuple=RemoveBraces
								BreakParams=CurrTuple.split(',')
								if(len(BreakParams)!=3):
									print "\n\t Woah! "+str(len(BreakParams))
								else:
									BreakParams[0]=int(WhiteSpace(BreakParams[0]))
											
						"""				
									#print "\n\t "+str((BreakParams))
	

def main(argv):
        SiminstFile=''
        CacheSpecsFile=''
        debug=0
        verbose=False
        try:
           opts, args = getopt.getopt(sys.argv[1:],"i:c:h:v",["siminst","cachespecs","deubg","help","verbose"])
        except getopt.GetoptError:
                #print str(err) # will print something like "option -a not recognized"
           usage()
           sys.exit(2)
        #verbose=False   
        for opt, arg in opts:
           if opt == '-h':
              usage()
              sys.exit()
           elif opt in ("-i", "--siminst"):
              SiminstFile=arg
              print "\n\t Input file is "+str(SiminstFile)
           elif opt in ("-c", "--cachespecs"):
              CacheSpecsFile=arg
              print "\n\t Input file is "+str(SiminstFile)
           elif opt in ("-v","--verbose"):
           	verbose=False
	   else:  
		usage()
	if( (SiminstFile=='') or (CacheSpecsFile=='') ):
		usage()
	Inp=open(SiminstFile)
	Input=Inp.readlines()
	Inp.close()
	
	CSpecs=open(CacheSpecsFile)
	CacheSpecsInput=CSpecs.readlines()
	CSpecs.close()

	
	NumLines=len(Input)	
	CacheStats={}
	for LineNum in range(0,len(Input)):
		CurrLine=Input[LineNum]
		SysIDLine=re.match('\s*.*sysid.*',CurrLine)
		if SysIDLine:
			print "\n\t Found a sysid at line "+str(LineNum)
			SysID=re.match('\s*.*sysid(\d+)*.*',CurrLine)
			if SysID:
				print "\n\t SysID being detected is "+str(SysID.group(1))
				CacheStats[SysID.group(1)]={}
				offset=1
				CurrSysID=SysID.group(1)
				CacheStats[CurrSysID]['Hits']=[]
				CacheStats[CurrSysID]['Loads']=[]				
				for j in range(3):
					if( (j+LineNum) < (NumLines) ):
						CurrLine=Input[LineNum+j+offset]						
						if (j<2):
							#print "\n\t Processing line: "+str
							CacheStatsLine=re.match('\s*.*l.*\[',CurrLine)
							if CacheStatsLine:
								#print "\n\t CacheStatsLine: "+str(CacheStatsLine.group(0))
								Numbers=re.split('\[',CurrLine)
								if Numbers:
									if(j==0):
										if verbose:
											print "\n\t Format: Hits -- Total -- Hits "
									elif(j==1):
										if verbose:
											print "\n\t Format: Hits -- Total -- Loads "
									for CurrNum in Numbers:
										GetStats=re.match('\s*(\d+)*\/(\d+)*',CurrNum)
										if GetStats:
											if(j==0):
												if verbose:
													print " "+str(GetStats.group(2))+"\t"+str(GetStats.group(1)) 
												Dummy=[]
												Dummy.append(GetStats.group(1))
												Dummy.append(GetStats.group(2))
												CacheStats[CurrSysID]['Hits'].append(Dummy)
											#CacheStats[CurrSysID]	
											elif(j==1):
												if verbose:
													print " "+str(GetStats.group(2))+"\t"+str(GetStats.group(1))
												Dummy=[]
												Dummy.append(GetStats.group(1))
												Dummy.append(GetStats.group(2))
												CacheStats[CurrSysID]['Loads'].append(Dummy)

						else:
							HybridCacheLine=re.match('\s*HybridCache',CurrLine)
							if HybridCacheLine:
								#print "\n\t --*-- HybridLine: "+str(CurrLine)
								Numbers=re.split('\[',CurrLine)
								if Numbers:
									FieldNum=-1
									for CurrNum in Numbers:
										FieldNum+=1
										GetStats=re.match('\s*(\d+)*\/(\d+)*',CurrNum)
										if GetStats:
											if(FieldNum==1): 
												Dummy=[]
												Dummy.append(GetStats.group(1))
												Dummy.append(GetStats.group(2))
												CacheStats[CurrSysID]['Hits'].append(Dummy)						
												if verbose:
													print "\n\t --*--- Hits--Total "+str(GetStats.group(2))+"\t"+str(Dummy[1])
											else:
												if verbose:
													print "\n\t --*--- Loads--Total "+str(GetStats.group(2))+"\t"+str(GetStats.group(1)) 
												Dummy=[]
												Dummy.append(GetStats.group(1))
												Dummy.append(GetStats.group(2))
												CacheStats[CurrSysID]['Loads'].append(Dummy)					


	for keys in CacheStats:
		LevelNum=0
		#print "\n\t SysID: "+str(keys)
		#print "\n\t Hits-format --Total-- --Hits--" 
		#CacheStats[keys]['Misses']=[]
		for CurrLevel in CacheStats[keys]['Hits']:
			CurrLevel.append(int(CurrLevel[1])-int(CurrLevel[0]))
			#print " "+str(CurrLevel[1])+"\t "+(CurrLevel[0])
		#print "\n\t Loads-format --Total-- --Loads--" 
		for CurrLevel in CacheStats[keys]['Loads']:
			CurrLevel.append(int(CurrLevel[1])-int(CurrLevel[0]))
			#print " "+str(CurrLevel[1])+"\t "+(CurrLevel[0])					
	
	
	for keys in CacheStats:
		LevelNum=0
		print "\n\t SysID: "+str(keys)
		print "\n\t Hits-format --Total-- --Hits--Misses" 
		for CurrLevel in CacheStats[keys]['Hits']:
			print " "+str(CurrLevel[1])+"\t "+str(CurrLevel[0])+"\t "+str(CurrLevel[2])
		print "\n\t Loads-format --Total-- --Loads--Stores" 
		for CurrLevel in CacheStats[keys]['Loads']:
			print " "+str(CurrLevel[1])+"\t "+str(CurrLevel[0])+"\t "+str(CurrLevel[2])
	CacheSpecs=ReadCacheSpecs(CacheSpecsInput)

if __name__=="__main__":
	main(sys.argv[1:])

# /usr/bin/python 
import sys,re,getopt

def usage():
	print "\n\t ExtractCacheStats.py -i <siminst-file> "
	sys.exit()
 
def main(SiminstFile,ReqSysID,verbose=0):
 	Inp=open(SiminstFile)
	Input=Inp.readlines()

	NumLines=len(Input)	
	CacheStats={}
	for LineNum in range(0,len(Input)):
		CurrLine=Input[LineNum]
		SysIDLine=re.match('\s*.*sysid.*',CurrLine)
		if SysIDLine:
			if verbose:
				print "\n\t Found a sysid at line "+str(LineNum)
			SysID=re.match('\s*.*sysid(\d+)*.*',CurrLine)
			if SysID:
				if verbose:
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
	ReqStats={}
	ReqStats['Hits']=[]
	ReqStats['Loads']=[]
 	for keys in CacheStats:
		LevelNum=0
 		#print "\n\t Requested SysID: "+str(ReqSysID)+" current key: "+str(keys)+" -"
		if(int(keys)==int(ReqSysID)):
			#print "\n\t SysID: "+str(keys)
			#print "\n\t Hits-format --Total-- --Hits--" 
			for CurrLevel in CacheStats[keys]['Hits']:
				#print " "+str(CurrLevel[1])+"\t "+(CurrLevel[0])
				ReqStats['Hits'].append(CurrLevel)
			#print "\n\t Loads-format --Total-- --Loads--" 
			for CurrLevel in CacheStats[keys]['Loads']:
				#print " "+str(CurrLevel[1])+"\t "+(CurrLevel[0])					
				ReqStats['Loads'].append(CurrLevel)
				
			print "\n\t ReqStats--levels: "+str(len(ReqStats['Hits']))
	return ReqStats

if __name__=="__main__":
	main(sys.argv[1:])

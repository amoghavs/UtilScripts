# /usr/bin/python 
import sys,re,getopt

def usage():
	print "\n\t ExtractCacheStats.py -i <siminst-file> -c <cache-specification-file>"
	sys.exit()
	
def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output

def ExtractSpecs(CurrLevelDict,CurrSpec,SpecToExtract,NumParams):
	CurrLevel=0
	#CurrLevelDict[CurrLevel]={}
	for CurrTuple in SpecToExtract:
		RemoveBraces=re.sub('\s*\(','',CurrTuple);
		if RemoveBraces:
			CurrTuple=RemoveBraces
			BreakParams=CurrTuple.split(',')
			if(len(BreakParams)!=NumParams):
				print "\n\t Woah! "+str(len(BreakParams))
			else:
				ExtractLevel=int(RemoveWhiteSpace(BreakParams[0]))
				if(ExtractLevel>CurrLevel):
					CurrLevel=ExtractLevel
				if(not(CurrLevel in CurrLevelDict)):
					CurrLevelDict[CurrLevel]={}
				if(not(CurrSpec in CurrLevelDict[CurrLevel])):
					CurrLevelDict[CurrLevel][CurrSpec]=[]
					#print "\n\t CurrSpec-- "+str(CurrSpec)
				BreakParams[1]=RemoveWhiteSpace(BreakParams[1])
				BreakParams[2]=re.sub('\)\s*$','',BreakParams[2])
				BreakParams[2]=float(RemoveWhiteSpace(BreakParams[2]))
				if(NumParams>3):
					BreakParams[3]=re.sub('\)\s*$','',BreakParams[3])
					BreakParams[3]=int(RemoveWhiteSpace(BreakParams[3]))
					CurrLevelDict[CurrLevel][CurrSpec].append((BreakParams[1],BreakParams[2],BreakParams[3]))		
				else:
					CurrLevelDict[CurrLevel][CurrSpec].append((BreakParams[1],BreakParams[2]))		
	
def ReadCacheSpecs(CacheSpecsInp):
	CacheSpecs={}
	SysIDSpecs={}
	LineNum=0
	CacheSpecs['SysID']=[]
	for CurrLine in CacheSpecsInp:
		LineNum+=1
		CheckComment=re.match('^\s*\#',CurrLine)
		Meh=0
		if CheckComment:
			Meh=0
			#print "\n\t Line-num is comment "+str(LineNum)	
		else:
			CheckEmptyLine=re.match('^\s*$',CurrLine)
			if CheckEmptyLine:
				Meh=0
				#print "\n\t Line-num is empty "+str(LineNum)	
			else:
				SeperateColon=re.split(';',CurrLine)
				if(len(SeperateColon)!=5):
					print "\n\t Format error: expected 5 fields, which are seperated by 4 semicolons in line "+str(LineNum)
					sys.exit()	
				else:
					CurrSysID=RemoveWhiteSpace(SeperateColon[0])
					CacheSpecs['SysID'].append(CurrSysID)	
					NumCacheLevels=int(RemoveWhiteSpace(SeperateColon[1]))
					Hybrid=int(RemoveWhiteSpace(SeperateColon[2]))
					if(Hybrid):
						NumCacheLevels+=1	
					#print "\n\t Curr Sys ID is: "+str(CurrSysID)+" NumCache: "+str(NumCacheLevels)+" Hybrid "+str(Hybrid) 
					CacheSpecs[CurrSysID]={}
					SysIDSpecs[CurrSysID]={}			
					ResponseDelay=re.split('\),',SeperateColon[3])
					SysIDSpecs[CurrSysID]['NumCache']=NumCacheLevels
					SysIDSpecs[CurrSysID]['Hybrid']=Hybrid
					#print "\n\t (len(ResponseDelay)): "+str((len(ResponseDelay)))
					if( (len(ResponseDelay)) >= (NumCacheLevels+1)):
						#print "\n\t Found "+str(len(ResponseDelay))+" tuples for memory-response-delay specs! "
						ExtractSpecs(CacheSpecs[CurrSysID],'Latency',ResponseDelay,3)
					EnergyDelay=re.split('\),',SeperateColon[4])
					if( (len(EnergyDelay)) >= (NumCacheLevels+1)):
						#print "\n\t Found "+str(len(EnergyDelay))+" tuples for memory-response-energy specs! "
						ExtractSpecs(CacheSpecs[CurrSysID],'Energy',EnergyDelay,4)
						
	return (CacheSpecs,SysIDSpecs)						

def TotalMemoryAccessTimeNEnergy(CacheStats,CacheSpecs,SysIDSpecs,Results,verbose):
	for CurrSysID in CacheStats:
		Results[CurrSysID]={}
		Results[CurrSysID]['Latency']=0.0
		Results[CurrSysID]['Energy']=0.0
		SpecsKeys=('Latency','Energy')
		
		Stats=[]
		StatsLevel=0
		NumStatsLevels=len(CacheStats[CurrSysID]['Hits'])
		#print "\n\t NumStatsLevels: "+str(NumStatsLevels)
		for CurrLevel in range(NumStatsLevels):
			CurrLevelStats=[]
			CurrLevelStats.append(CacheStats[CurrSysID]['Hits'][CurrLevel])
			CurrLevelStats.append(CacheStats[CurrSysID]['Loads'][CurrLevel])
			Stats.append(CurrLevelStats)
			#print "\n\t Level: "+str(CurrLevel)

		for CurrSpec in SpecsKeys:
			Accumulator=0.0
			if CurrSysID in CacheSpecs:
				#print "\n\t len(CacheSpecs[CurrSysID]): "+str(len(CacheSpecs[CurrSysID]))+" len(Stats) "+str(len(Stats))
				if( ( len(CacheSpecs[CurrSysID]) == len(Stats) ) or ( len(CacheSpecs[CurrSysID]) == (len(Stats)+1) ) ):
					#for CurrLevel in CacheSpecs[CurrSysID]:
					for CurrLevel in range(1,NumStatsLevels+1):
						#print "\n\t CurrLevel: "+str(CurrLevel)+" len(CacheSpecs[CurrSysID]) "+str(len(CacheSpecs[CurrSysID]))
						CurrLevelStats=Stats[CurrLevel-1] #[CurrSysID]['Loads']
						if(CurrSpec=='Latency'):
							for CurrTuple in CacheSpecs[CurrSysID][CurrLevel][CurrSpec]:
								#print "\n\t CurrLevel "+str(CurrLevel)+" CurrTuple "+str(CurrTuple)+" Accumulator "+str(Accumulator)+" len(CacheSpecs[CurrSysID][CurrLevel][CurrSpec]): "+str(len(CacheSpecs[CurrSysID][CurrLevel][CurrSpec]))						
								if(CurrTuple[0]=='rw'):
									Accumulator+=( CurrTuple[1] *(CurrLevelStats[0][0] + 2* CurrLevelStats[0][2]) )
								elif(CurrTuple[0]=='r'):
									Accumulator+=( CurrTuple[1] * CurrLevelStats[1][0] )
								elif(CurrTuple[0]=='w'):
									Accumulator+=( CurrTuple[1] * CurrLevelStats[1][2] )
						elif(CurrSpec=='Energy'):
							for CurrTuple in CacheSpecs[CurrSysID][CurrLevel][CurrSpec]:
								#print "\n\t CurrLevel "+str(CurrLevel)+" CurrTuple "+str(CurrTuple)+" Accumulator "+str(Accumulator)						
								if(CurrTuple[0]=='rw'):
									Accumulator+=( CurrTuple[1] * CurrTuple[2] * 8 * (CurrLevelStats[0][0] + 2* CurrLevelStats[0][2]) )
								elif(CurrTuple[0]=='r'):
									Accumulator+=( CurrTuple[1] * CurrTuple[2] * 8 * CurrLevelStats[1][0] )
								elif(CurrTuple[0]=='w'):
									Accumulator+=( CurrTuple[1] * CurrTuple[2] * 8 * CurrLevelStats[1][2] )							
					if( len(CacheSpecs[CurrSysID]) == (len(Stats)+1) ):
						CurrLevelStats=Stats[NumStatsLevels-1]
						for CurrTuple in CacheSpecs[CurrSysID][CurrLevel][CurrSpec]:
							#CurrTuple=CacheSpecs[CurrSysID][NumStatsLevels+1][CurrSpec]
							print "\n\t CurrTuple: "+str(CurrTuple)+" len: "+str(len(CurrTuple))+" CurrLevel: "+str(NumStatsLevels+1)+" {CurrTUple} "+str(CacheSpecs[CurrSysID][1][CurrSpec])
							if(CurrSpec=='Latency'):
								Accumulator+=( CurrTuple[1] * 1 ) #* ( CurrLevelStats[0][2]) )
							elif(CurrSpec=='Energy'):
								Accumulator+=( CurrTuple[1] * CurrTuple[2] * 8 * ( CurrLevelStats[0][2]) )
					
					Results[CurrSysID][CurrSpec]=Accumulator
					if verbose:
						print "\n\t SysID: "+str(CurrSysID)+" CurrSpec "+str(CurrSpec)+" Accumulator "+str(Results[CurrSysID][CurrSpec])
				else:
					print "\n\t ERROR: Stats available for levels: "+str(len(Stats))+" specifications provide info for "+str(len(CacheSpecs[CurrSysID]))+" hybrid-level "+str(SysIDSpecs[CurrSysID]['Hybrid'])
					sys.exit()
			else:
				print "\n\t FatalError: CacheSpecs is not provided for SysID: "+str(CurrSysID)
				sys.exit()


def main(argv):
        SiminstFileSet=''
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
              SiminstFileSet=arg
              print "\n\t Input file is "+str(SiminstFileSet)
           elif opt in ("-c", "--cachespecs"):
              CacheSpecsFile=arg
              print "\n\t CacheSpecsFile is "+str(CacheSpecsFile)
           elif opt in ("-v","--verbose"):
           	verbose=False
	   else:  
		usage()
	if( (SiminstFileSet=='') or (CacheSpecsFile=='') ):
		usage()

	Inp=open(SiminstFileSet)
	InputFileSet=Inp.readlines()
	Inp.close()
	
	CSpecs=open(CacheSpecsFile)
	CacheSpecsInput=CSpecs.readlines()
	CSpecs.close()

	
	NumFiles=len(InputFileSet)	
	CacheStats={}
	
	for CurrInpFile in InputFileSet:
		TempFileName=RemoveWhiteSpace(CurrInpFile)
		if(TempFileName):
			Inp=open(TempFileName)
			Input=Inp.readlines()
			Inp.close()
			NumLines=len(Input)
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
						if verbose:
							print "\n\t SysID.group(0): "+str(SysID.group(0))+" SysID.group(1): "+str(SysID.group(1))
						CurrSysID=RemoveWhiteSpace(SysID.group(1))
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
														Dummy.append(int(GetStats.group(1)) )
														Dummy.append(int(GetStats.group(2)) )
														CacheStats[CurrSysID]['Hits'].append(Dummy)
													#CacheStats[CurrSysID]	
													elif(j==1):
														if verbose:
															print " "+str(GetStats.group(2))+"\t"+str(GetStats.group(1))
														Dummy=[]
														Dummy.append(int(GetStats.group(1)) )
														Dummy.append(int(GetStats.group(2)) )
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
														Dummy.append(int(GetStats.group(1)) )
														Dummy.append(int(GetStats.group(2)) )
														CacheStats[CurrSysID]['Hits'].append(Dummy)						
														if verbose:
															print "\n\t --*--- Hits--Total "+str(GetStats.group(2))+"\t"+str(Dummy[1])
													else:
														if verbose:
															print "\n\t --*--- Loads--Total "+str(GetStats.group(2))+"\t"+str(GetStats.group(1)) 
														Dummy=[]
														Dummy.append(int(GetStats.group(1)) )
														Dummy.append(int(GetStats.group(2)) )
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
				if verbose:
					print "\n\t SysID: "+str(keys)
					print "\n\t Hits-format --Total-- --Hits--Misses" 
					for CurrLevel in CacheStats[keys]['Hits']:
						print " "+str(CurrLevel[1])+"\t "+str(CurrLevel[0])+"\t "+str(CurrLevel[2])
					print "\n\t Loads-format --Total-- --Loads--Stores" 
					for CurrLevel in CacheStats[keys]['Loads']:
						print " "+str(CurrLevel[1])+"\t "+str(CurrLevel[0])+"\t "+str(CurrLevel[2])

			(CacheSpecs,SysIDSpecs)=ReadCacheSpecs(CacheSpecsInput)
			Results={}
			TotalMemoryAccessTimeNEnergy(CacheStats,CacheSpecs,SysIDSpecs,Results,verbose)
			print "\n\t CurrInpFile: "+str(TempFileName)
			print "\n\t SysID\t\t\t\t HitRate\t\t AMAT "
			for keys in CacheStats:
				HitRateString=''
				for CurrLevel in CacheStats[keys]['Hits']:
					HitRate=float( float(CurrLevel[0])/(CurrLevel[1]) )
					HitRateString+='\t'+str(round(HitRate,5))
				#print "\n\t SysID: "+str(keys)+" HitRate: "+str(HitRateString)+" AMAT: "+str(Results[keys]['Latency'])
				print "\n\t "+str(keys)+"\t"+str(HitRateString)+"\t"+str(Results[keys]['Latency'])
	
	print"\n"


if __name__=="__main__":
	main(sys.argv[1:])
	


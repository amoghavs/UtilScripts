#! /usr/bin/python
import sys,getopt,subprocess,re,math,commands,time,copy,random

def usage():
	print "\t python GenerateHitRateExplore.py -i/--input <Sample-Input-File> -m/--memorylevel <Memory being used> -n/--numoperands <NumOperands in an Exprn>" 
	#-m/--mod <Index-mod> -r/--ratecontrolbegin <RateControlBegin> -q/--ratecontrolend <RateControlEnd> 
	print "\t Accepted inputs for memory level: L1,L2,L3,Mem "
	print "\n"
	sys.exit()
	
def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output

def RemoveBraces(Input):
	temp=re.sub('^\s*\(*','',Input)
	Output=re.sub('\)\s*$','',temp)
	#print "\n\t RemoveBraces--Input: "+str(Input)+" tmp: "+str(temp)+" Output "+str(Output)
	return Output

def grep(*matches):
    """Returns a generator function that operates on an iterable:
        filters items in the iterable that match any of the patterns.

    match: a callable returning a True value if it matches the item

    >>> import re
    >>> input = ["alpha\n", "beta\n", "gamma\n", "delta\n"]
    >>> list(grep(re.compile('b').match)(input))
    ['beta\n']
    """
    def _do_grep_wrapper(*matches):
        def _do_grep(lines):
            for LineNum,line in enumerate(lines):
                for match in (matches):
                    if match(line):
                        yield (line,LineNum)
                        break
        return _do_grep
    return _do_grep_wrapper(*matches)

def FileOpen(FileName,options=''):
	if(options==''):
		try:
			FileHandle=open(FileName)
		except IOError:
		 	print 'cannot open', FileName
	else:
		try:
			FileHandle=open(FileName,options)
		except IOError:
			print 'cannot open', FileName
			
	FileContents=FileHandle.readlines()
	FileHandle.close()
	return FileContents		

def main(argv):
	InputFileName=''
	MemoryLevel=''
	NumOperands=''
	try:
		opts, args = getopt.getopt(sys.argv[1:],"i:m:n:",["input=","memorylevel=","numoperands="])	
	except getopt.GetoptError:
		#print str(err) # will print something like "option -a not recognized"
		usage()
	for opt, arg in opts:
		#print "\n\t Opt: "+str(opt)+" argument "+str(arg)	
		if opt in('-i', "--input"):
			InputFileName=RemoveWhiteSpace(arg)
			print "\t Input file name: "+str(InputFileName)
		elif opt in('-m', "--memorylevel"):
			MemoryLevel=RemoveWhiteSpace(arg)
			print "\t Memory level name: "+str(MemoryLevel)
		elif opt in('-n',"--numoperands"):
			NumOperands=int(RemoveWhiteSpace(arg))
			print "\t NumOperands : "+str(NumOperands)
		else:
			usage()
	if(InputFileName==''):
		usage()
	if(NumOperands==''):
		NumOperands=1
		print "\t INFO: Assuming default num-operands: "+str(NumOperands)
	if(MemoryLevel==''):
		MemoryLevel='L1'
		print "\t INFO: Assuming default memory level: "+str(MemoryLevel)
		
	print "\n"
	LevelIndexMod=15
	Begin={};End={}
	Begin['LevelIndexMod']=15
	End['LevelIndexMod']=15
	Begin['RateControl']=0
	End['RateControl']=15
	#Begin['CacheLevel']=
	#End['CacheLevel']=
	
	SizeIdx=2 # Increment from 'mem-level' in FileName
	DSIdx=4
	OpsIdx=6
	PANIdx=8
	BreakdownParams=re.split('\_',InputFileName)
	ArraySize=''
	DS=''
	Ops=''
	PAN=''
	
	StopIdx=-1
	Prefix=''
	MemLevelParams=''
	for Idx,CurrParam in enumerate(BreakdownParams):
		if(CurrParam==MemoryLevel):
			print "\t Found MemoryLevel in param: "+str(CurrParam)
			print "\t Memory level at index: "+str(Idx)
			ArraySize=int(RemoveWhiteSpace(BreakdownParams[Idx+SizeIdx]))
			DS=RemoveWhiteSpace(BreakdownParams[Idx+DSIdx])
			Ops=RemoveWhiteSpace(BreakdownParams[Idx+OpsIdx])
			print "\t BreakdownParams[Idx+PANIdx] "+str(BreakdownParams[Idx+PANIdx])
			print "\t ArraySize: "+str(ArraySize)+" DS "+str(DS)+" Ops "+str(Ops)+" PAN: "+str(PAN) 
			MemLevelParams=str(CurrParam)+'_Size_'+str(ArraySize)+'_DS_'+str(DS)+'_'
			PrefixStopIdx=Idx+DSIdx+1
			SuffixStartIdx=Idx+PANIdx+1
			break
		else:
			Prefix+=str(CurrParam)+'_'

	Length=len(BreakdownParams)		
	Suffix=''
	#for Idx in range(0,PrefixStopIdx):
	#	Prefix+=BreakdownParams[Idx]+'_'
	for Idx in range(SuffixStartIdx,Length-1):	
		CurrParam=BreakdownParams[Idx]		
		Temp=str(CurrParam)+'_'
		Suffix+=str(Temp)

	Suffix+=str(BreakdownParams[Length-1])
	print "\t Prefix: "+str(Prefix)+" Suffix "+str(Suffix)

	HitRateControlParam='\#define\ '+str(MemoryLevel)+'HitRateControl '
	THitRateControlParam=str(MemoryLevel)+'HitRateControl'
	IterationVarModParam='\#define\ '+str(MemoryLevel)+'ExtractBit '
	TIterationVarModParam=str(MemoryLevel)+'ExtractBit'
	for CurrLevelIndexMod in range(Begin['LevelIndexMod'],End['LevelIndexMod']+1):
		for CurrRateControl in range(Begin['RateControl'],End['RateControl']+1):
			CurrPAN=(100-int( (100/CurrLevelIndexMod)*(CurrRateControl)) );
			OpsTerm=''
			if(NumOperands==0):
				OpsTerm='Ops_0'
			else:
				for CurrIdx in range(NumOperands-1):
					if(CurrIdx>0):
						OpsTerm+='o'
					else:
						OpsTerm+='O'
				OpsTerm='Ops_'+str(OpsTerm)

			print "\t CurrPAN: "+str(CurrPAN)+" MemLevelParams "+str(MemLevelParams)
			NewFileName=str(Prefix)+str(MemLevelParams)+str(OpsTerm)+'_PAN_'+str(CurrPAN)+'_'+str(Suffix)
			CpCmd='cp '+str(InputFileName)+' '+str(NewFileName)
			print "\t CpCmd: "+str(CpCmd)
		
			commands.getoutput(CpCmd)
	
		        NewFile=FileOpen(NewFileName)	
			GrepOutput=list(grep(re.compile('\s*\.*RandomVar').match)(NewFile))
			#print "\t GrepOutput "+str(GrepOutput)
			for CurrTuple in GrepOutput:
				CurrLine=NewFile[CurrTuple[1]]
				SplitLine=re.split('=',CurrLine)
				if(len(SplitLine)>=2):
					LHS=SplitLine[0]
					RHSSplit=re.split('\)',SplitLine[1])
					for CurrEle in RHSSplit:
						StreamFound=re.match('.*Stream.*',CurrEle)
						if(StreamFound):
							#print "\t group: "+str(StreamFound.group(0))
							VarStreamVar=re.split('\[',StreamFound.group(0))
							if(len(VarStreamVar)>=2):
								TempVarStreamVar=RemoveBraces(RemoveBraces(VarStreamVar[0]))
								ExtractVarNum=re.match('.*Var(\d+)*.*',TempVarStreamVar)
								if(ExtractVarNum):
									#print "\t StreamVar "+str(TempVarStreamVar)+" -- "+str(ExtractVarNum.group(1))
									VarNum=ExtractVarNum.group(1)
									ReconstructExprn=LHS+' = ( (int) '
									for Curr in range(NumOperands):
										if(Curr>0):
											ReconstructExprn+=' | '
										Term='( Var'+str(VarNum)+'_Stream0_Operand0[ RandomVar'+str(VarNum)+' + ( OpDiffVar'+str(VarNum)+' * '+str(Curr)+') ] )'
										#print "\t Term: "+str(Term)
										ReconstructExprn+=str(Term)
									ReconstructExprn+=' ) '
									NewFile[CurrTuple[1]]=ReconstructExprn
								#print "\t ReconstructExprn: "+str(ReconstructExprn)
			#print "\n\t HitRateControlParam: "+str(THitRateControlParam)+"---"
			FindHitRateControl=list(grep(re.compile('.*'+re.escape(THitRateControlParam)+'.*').match)(NewFile))
			#print "\t FindHitRateControl: "+str(FindHitRateControl)
			for CurrEle in FindHitRateControl:
				IfDef=re.match('.*define.*',CurrEle[0])
				if(IfDef):
					ReconstructLine='\t #define '+str(THitRateControlParam)+' '+str(CurrRateControl)+'\n'
					print "\t 1. ReconstructLine: "+str(ReconstructLine)
					NewFile[CurrEle[1]]=ReconstructLine

			#print "\t IterationVarModParam "+str(TIterationVarModParam)
			FindIterationVarModParam=list(grep(re.compile('.*'+re.escape(TIterationVarModParam)+'.*').match)(NewFile))	
			#print "\t FindIterationVarModParam: "+str(FindIterationVarModParam)
			for CurrEle in FindIterationVarModParam:
				IfDef=re.match('.*define.*',CurrEle[0])
				if(IfDef):
					ReconstructLine='\t #define '+str(TIterationVarModParam)+' '+str(CurrLevelIndexMod)+'\n'
					print "\t 2. ReconstructLine: "+str(ReconstructLine)
					NewFile[CurrEle[1]]=ReconstructLine
			FindNumOperandsVar=list(grep(re.compile('\s*int\ NumOperandsVar.*').match)(NewFile))
			for CurrTuple in FindNumOperandsVar:
				#print "\t CurrLine: "+str(CurrTuple[0])
				ExtractLHS=re.split('\=',CurrTuple[0])
				if(len(ExtractLHS)>=2):
					ReconstructLine=ExtractLHS[0]+' = '+str(NumOperands)+';\n'
					print "\t 3. ReconstructLine: "+str(ReconstructLine)
					NewFile[CurrEle[1]]=ReconstructLine
			#print "\t FindNumOperands: "+str(FindNumOperandsVar)
			WriteNewFile=open(NewFileName,'w')
			print "\t Rewriting file: "+str(NewFileName)
			for CurrLine in NewFile:
				WriteNewFile.write(CurrLine)
			sys.exit()	

if __name__=="__main__":
	main(sys.argv[1:])

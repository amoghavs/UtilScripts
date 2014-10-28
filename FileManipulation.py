#!/usr/bin/python
import sys,getopt,subprocess,re,math,commands,time,copy,random

def usage():
	print "\n\t python FileManipulation.py has following utilities and the respective inputs are displayed along! "
	print "\t CopyMultipleTimes -i/--input <InputFile> -n/--numrepeat <Number-of-times-a-line-will-be-repeated> -o/--output <Output-file> "
	print "\t CompareAndSyncFiles -a/--file1 <Input-File-1> -b/--file2 <Input-File-2 to which Input-File-1 will be synced> -f/--field1 <field of file 'a' > -g/--field2 <field of file 'b'> "
	print "\t ValueRelativeToBase -i/--input <Input File> -o/--output <Output File> \n\t\t Method expects first line to have a header and is currently looking for three parameters. "
	print "\n\n\t Chosing utility: \n\t\t -c/--copy: CopyMultipleTimes \n\t\t -s/--sync: CompareAndSyncFiles -r/--relative: ValueRelativeToBase -r/--relative: ValueRelativeToBase "
	print "\n"
	sys.exit()
	
def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output

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

def CopyMultipleTimes(InputFileName,OutputFileName,NumRepeat):
	if(OutputFileName==''):
		OutputFileName='Repeated_'+str(InputFileName)
		print "\t INFO: Using default output file name: "+str(OutputFileName)
	if(NumRepeat==''):
		NumRepeat=3
		print "\t INFO: Using "+str(NumRepeat)+" as default number of times a line will be repeated "
	else:
		if( not ( (NumRepeat==int(NumRepeat)) and (NumRepeat>0) ) ):
			print "\t NumRepeat: "+str(NumRepeat)+" is illegal!! "
			sys.exit()
	
	InputFile=FileOpen(InputFileName)
	NumLines=len(InputFile)
	OutputFile=open(OutputFileName,'w')
	print "\t Input file has "+str(NumLines)+" number of lines! "		
	for CurrLine in InputFile:
		for i in range(NumRepeat):
			OutputFile.write(CurrLine)
	OutputFile.close()

def ValueRelativeToBase(InputFileName,OutputFileName):
	if(OutputFileName==''):
		OutputFileName='RelativeVal_'+str(InputFileName)
		print "\t INFO: Using default output file name: "+str(OutputFileName)
	
	InputFile=FileOpen(InputFileName)
	NumLines=len(InputFile)
	OutputFile=open(OutputFileName,'w')
	print "\t Input file has "+str(NumLines)+" number of lines! "		
	BaseFreq=2600000
	
	BaseValue='ACPOWER' #'Runtime'
	Params=('Frequency','FileName',BaseValue)
	Fields={}
	LineOne=InputFile[0]
	BreakParams=re.split('\t',LineOne)
	for ParamIdx,CurrParam in enumerate(BreakParams):
		CurrParam=RemoveWhiteSpace(CurrParam)
		for CurrNeededParam in Params:
			if(CurrParam==CurrNeededParam):
				Fields[CurrParam]=ParamIdx
				
	for CurrField in Fields:
		print "\t Field: "+str(CurrField)+" Idx: "+str(Fields[CurrField])

	LargerFieldNum=-1
	
	for CurrField in Fields:
		if( Fields[CurrField] > LargerFieldNum):
			LargerFieldNum=Fields[CurrField]
			print "\t LargerFieldNum: "+str(LargerFieldNum)

	Header=InputFile[0]		
	del InputFile[0]			
	
	RelatedFiles={}
	ValuesForFiles={}
	for LineNum,CurrLine in enumerate(InputFile):
		BreakParams=re.split('\t',CurrLine)
		if(len(BreakParams)>=(LargerFieldNum+1) ):
			ValuesForFiles={}
			Freq=float(RemoveWhiteSpace(BreakParams[Fields['Frequency']])) #int(RemoveWhiteSpace(BreakParams[Fields['Frequency']]))
			VBaseValue=float(RemoveWhiteSpace(BreakParams[Fields[BaseValue]]))
			FileName=RemoveWhiteSpace(BreakParams[Fields['FileName']])		
			print "\t Freq: "+str(Freq)+" BaseValue: "+str(VBaseValue)
			ValuesForFiles['Frequency']=Freq
			ValuesForFiles[BaseValue]=VBaseValue
			ValuesForFiles['RestOfLine']=RemoveWhiteSpace(CurrLine)
			ValuesForFiles['LineNum']=LineNum
			
			if( not( FileName in RelatedFiles) ):
				RelatedFiles[FileName]=[]
			#if(int(Freq)==BaseFreq):
			if(float(Freq)==BaseFreq):
				RelatedFiles[FileName].insert(0,ValuesForFiles)
				print "\t ** BaseFreq's values inserted in front "
			else:
				RelatedFiles[FileName].append(ValuesForFiles)
				print "\t Non-BaseFreq's values inserted in front "
		#else:
		#	print "\t Nodappa illi yeno problem ide: "+str(CurrLine)
	print "\n"
	RealignFile={}
	#Lines
	for CurrFile in RelatedFiles:
		print "\t File: "+str(CurrFile)+" found "+str(len(RelatedFiles[CurrFile]))+" such files"
		FoundBaseFreq=(RelatedFiles[CurrFile][0]['Frequency']==BaseFreq)
		if(FoundBaseFreq):
			BaseValueNum=(RelatedFiles[CurrFile][0][BaseValue]) 
			for CurrValues in (RelatedFiles[CurrFile]):
				CurrValues['RelativeValue']=( CurrValues[BaseValue] / BaseValueNum)
				#print "\t Freq: "+str(CurrValues['Frequency'])+" FoundBase: "+str(FoundBaseFreq)+" RelativeValue "+str(CurrValues['RelativeValue'])
				RealignFile[CurrValues['LineNum']]=CurrValues['RelativeValue']

	OutputFile.write(str(Header)+"\n")		
	for LineNum,OldLine in enumerate(InputFile):
		CurrOldLine=RemoveWhiteSpace(OldLine)
		if( LineNum in RealignFile):
			#print "\t LineNum: "+str(LineNum)+" "+str(RealignFile[LineNum])
			OutputFile.write(" "+str(CurrOldLine)+"\t"+str(RealignFile[LineNum])+"\n")
	OutputFile.close()

def SyncFiles(CompareFile1Name,CompareFile2Name,Field1,Field2):
	if(Field1==''):	
		Field1=0
		print "\t INFO: Assuming Field1 to default value: "+str(Field1)

	if(Field2==''):	
		Field2=0
		print "\t INFO: Assuming Field2 to default value: "+str(Field2)
	TempFile1Name=CompareFile1Name
	TempFile2Name=CompareFile2Name	
	CheckLog=re.match('(.*)\.log.*',CompareFile1Name)
	if CheckLog: TempFile1Name=(CheckLog.group(1))	
	CheckLog=re.match('(.*)\.log.*',CompareFile2Name)
	if CheckLog: TempFile2Name=(CheckLog.group(1))	
	
	OutputFileName='SyncFile_'+str(TempFile1Name)+'_'+str(TempFile2Name)+'.log'
	OutputFile=open(OutputFileName,'w')
	print "\t In Sync method.. Compare1 file: "+str(CompareFile1Name)+" Field1 "+str(Field1)
	print "\t\t\t  Compare2 file: "+str(CompareFile2Name)+" Field2 "+str(Field2)
	print "\t\t\t  Output file: "+str(OutputFileName)
	
	CompareFile1=FileOpen(CompareFile1Name)
	CompareFile2=FileOpen(CompareFile2Name)
	NumLinesFile1=len(CompareFile1)
	NumLinesFile2=len(CompareFile2)
	
	LowerNumLines=0
	HigherNumLines=0
	if(NumLinesFile1!=NumLinesFile2):
		if(NumLinesFile1>NumLinesFile2):
			LowerNumLines=NumLinesFile2
			HigherNumLines=NumLinesFile1
			print "\t 1. LowerNumLines: "+str(LowerNumLines)+" HigherNumLines "+str(HigherNumLines)
		else:
			LowerNumLines=NumLinesFile1
			HigherNumLines=NumLinesFile2
			print "\t 2. LowerNumLines: "+str(LowerNumLines)+" HigherNumLines "+str(HigherNumLines)
	else:
		LowerNumLines=NumLinesFile1
		HigherNumLines=NumLinesFile2

	File2AdjustLineNum=0
	#sys.exit()
	for LineNum in range(HigherNumLines):
		TempLineFile1=CompareFile1[LineNum]
		TempLineFile2=CompareFile2[LineNum-File2AdjustLineNum]
		AllFieldsFile1=re.split('\t',TempLineFile1)
		AllFieldsFile2=re.split('\t',TempLineFile2)
		#print "\t "+str(LineNum)
		#print "\t NumFields-file1 "+str(len(AllFieldsFile1))+" file2 "+str(len(AllFieldsFile2))
		CurrField1=RemoveWhiteSpace(AllFieldsFile1[Field1])
		CurrField2=RemoveWhiteSpace(AllFieldsFile2[Field2])
		if(CurrField1!=CurrField2):
			print "\t Should Yank line num: "+str(LineNum+1)+" from file-1"
			print "\t "+str(LineNum)+" "+str(CurrField1)+"++"+str(CurrField2)+"--"
			File2AdjustLineNum+=1
			#sys.exit()
		else:
			OutputFile.write("\t"+str(TempLineFile1))
			#sys.exit()
	print "\t 3. LowerNumLines: "+str(LowerNumLines)+" HigherNumLines "+str(HigherNumLines)
		

def main(argv):
	InputFileName=''
	NumRepeat=''
	OutputFileName=''
	CompareFile1Name=''
	CompareFile2Name=''
	Field1=''
	Field2=''
	Copy=''
	Sync=''
	Relative=''
	try:
		opts, args = getopt.getopt(sys.argv[1:],"i:n:o:a:b:f:g:h:c:s:r:",["input=","numrepeat=","output=","file1=","file2=","field1=","field2=","field3=","copy=","sync=","relative="])	
	except getopt.GetoptError:
		#print str(err) # will print something like "option -a not recognized"
		usage()
	for opt, arg in opts:
		#print "\n\t Opt: "+str(opt)+" argument "+str(arg)	
		if opt in('-i', "--input"):
			InputFileName=RemoveWhiteSpace(arg)
			print "\t Input file name: "+str(InputFileName)
		elif opt in('-o', "--output"):
			OutputFileName=RemoveWhiteSpace(arg)
			print "\t Output file name: "+str(OutputFileName)
		elif opt in('-n', "--numrepeat"):
			NumRepeat=int(RemoveWhiteSpace(arg))
			print "\t Number of times a line will be repeated is: "+str(NumRepeat)	
		elif opt in('-a',"--file1"):		
			CompareFile1Name=RemoveWhiteSpace(arg)
			print "\t CompareFile1Name: "+str(CompareFile1Name)
		elif opt in('-b',"--file2"):		
			CompareFile2Name=RemoveWhiteSpace(arg)
			print "\t CompareFile2Name: "+str(CompareFile2Name)
		elif opt in('-f',"--field1"):		
			Field1=int(RemoveWhiteSpace(arg))
			print "\t Field1: "+str(Field1)
		elif opt in('-g',"--field2"):		
			Field2=int(RemoveWhiteSpace(arg))
			print "\t Field2: "+str(Field2)
		elif opt in('-h',"--field3"):		
			Field3=int(RemoveWhiteSpace(arg))
			print "\t Field3: "+str(Field3)			
		elif opt in ('-c','--copy'):
			Copy=int(RemoveWhiteSpace(arg))
			print "\t Copy option is "+str(Copy)
		elif opt in ('-s','--sync'):
			Sync=int(RemoveWhiteSpace(arg))
			print "\t Sync option is "+str(Sync)
		elif opt in ('-r','--relative'):
			Relative=int(RemoveWhiteSpace(arg))
			print "\t Relative option is "+str(Relative)

		else:
			usage()
	if( (Copy=='') and (Sync=='') and (Relative=='') ):
		usage()
	print "\t Copy: "+str(Copy)+" Sync "+str(Sync)+" Relative "+str(Relative)
	if( (Copy!='') and (Copy>0) ):
		print "\t Coming into copy eh? "
		if(InputFileName==''):
			usage()
		CopyMultipleTimes(InputFileName,OutputFileName,NumRepeat)
	if( (Sync!='') and (Sync>0) ):
		print "\t Coming over to Sync "
		if( (CompareFile1Name=='') or (CompareFile2Name=='') ):
			usage()
		else:
			SyncFiles(CompareFile1Name,CompareFile2Name,Field1,Field2)
	if((Relative!='') and (Relative>0)):
		print "\t Coming into relative "
		if( (InputFileName=='') ):
			usage()
		else:
			ValueRelativeToBase(InputFileName,OutputFileName)
		
		
	

if __name__=="__main__":
	main(sys.argv[1:])




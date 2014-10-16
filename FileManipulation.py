import sys,getopt,subprocess,re,math,commands,time,copy,random

def usage():
	print "\n\t python FileManipulation.py has following utilities and the respective inputs are displayed along! "
	print "\t CopyMultipleTimes -i/--input <InputFile> -n/--numrepeat <Number-of-times-a-line-will-be-repeated> -o/--output <Output-file> "
	print "\t CompareAndSyncFiles -a/-file1 <Input-File-1> -b/--file2 <Input-File-2 to which Input-File-1 will be synced> -f/-field1 <field in file1> -g/-field2 <field in file2> "
	print "\n\n\t Chosing utility: \n\t\t -c/--copy: CopyMultipleTimes \n\t\t -s/--sync: CompareAndSyncFiles "
	print "\n"
	sys.exit()
	
def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output

def FileOpen(FileName,options=''):
	if(options==''):
		FileHandle=open(FileName)
	else:
		FileHandle=open(FileName,options)
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
			print "\t "+str(LineNum)+" "+str(CurrField1)+" "+str(CurrField2)
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
	try:
		opts, args = getopt.getopt(sys.argv[1:],"i:n:o:a:b:g:f:c:s:",["input=","numrepeat=","output=","file1=","file2=","field1=","field2=","copy=","sync="])	
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
		elif opt in ('-c','--copy'):
			Copy=int(RemoveWhiteSpace(arg))
			print "\t Copy option is "+str(Copy)
		elif opt in ('-s','--sync'):
			Sync=int(RemoveWhiteSpace(arg))
			print "\t Sync option is "+str(Sync)
		else:
			usage()
	if( (Copy=='') and (Sync=='') ):
		usage()
	print "\t Copy: "+str(Copy)+" Sync "+str(Sync)
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

	

if __name__=="__main__":
	main(sys.argv[1:])




# /usr/bin/python 
import sys,re,getopt

def usage():
	print "\n\t StaticInfoExtraction.py -i <list of static-file> -b <list of BBs> -n Number-of-fields -s Stat-line-num -a Op1 index -b Op2 index. \n\t Optional inputs: -b <List of BBs> -d <debug:default=0> -o <Output-file> "
	sys.exit()
def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output
	
def main(argv):
        SourceFile=''
        debug=0
	OutFileName=''
	BBFileName=''
	FieldsFileName=''
        try:
           opts, args = getopt.getopt(sys.argv[1:],"i:b:f:o:h:v",["input=","bb=","fields=","output=""help=","verbose="])
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
              SourceFile=arg
              print "\n\t Input file is "+str(SourceFile)
	   elif opt in ("-b", "--listofbb"):
		BBFileName=RemoveWhiteSpace(arg)
		print "\n\t BBFile is: "+str(BBFileName)+" \n"
	   elif opt in ("-f","-fields"):
		FieldsFileName=RemoveWhiteSpace(arg)
		print "\n\t Fields file name "+str(FieldsFileName)
	   elif opt in ("-o","-output"):
		OutFileName=RemoveWhiteSpace(arg)
		print "\n\t Fields file name "+str(OutFileName)
	   elif opt in ("-d","-debug"):
		debugStr=RemoveWhiteSpace(arg)
		debug=int(debugStr)
		print "\n\t Debug option is "+str(debug)
	   elif opt in ("-v","-verbose"):	
	   	Verbose=int(RemoveWhiteSpace(Arg))
	   	
	   else:  
		usage()

	if( (SourceFile=='') or (BBFileName=='') ):
		usage()
		
	IpFile=open(SourceFile)
	Input=IpFile.readlines()
	IpFile.close()
			
	if( (OutFileName=='')):
		OutFileName='DefaultOutputFile.log'
		print "\t INFO: Default output file being used-- "+str(OutFileName)
	OutStream=open(OutFileName,'w')
        ListofFiles=[] 
	for CurrLine in Input:
		Temp=RemoveWhiteSpace(CurrLine)
		if(not(Temp=='')):
			ListofFiles.append(Temp)	       
	print "\n\t Number of files to process: "+str(len(ListofFiles))
	NumofFilestoProcess=len(ListofFiles)
	if(NumofFilestoProcess==0):
		print "\n\t ERROR: Number of files to process is "+str(NumofFilestoProcess)
		sys.exit()

	BBFileAvailable=-1
	if(BBFileName==''):
		BBFileAvailable=0
	else:
		BBFileAvailable=1

	ListofBBs=[]
	BBListAvailable=-1
	if BBFileAvailable:
	 IpFile=open(BBFileName)
	 BBFile=IpFile.readlines()
	 IpFile.close() 
	 for CurrLine in BBFile:
		Tmp=RemoveWhiteSpace(CurrLine)
		if(not(Tmp=='')):
			ListofBBs.append(Tmp)
	 print "\t Number of BBs to extract: "+str(len(ListofBBs))
	 if( len(ListofBBs)==0):
		BBListAvailable=0
	 else:
		BBListAvailable=1
	else:
		BBListAvailable=0
	
	RequestedFields={}
	if(FieldsFileName==''):
		print "\n\t Fields file is not provided. Hence following fields will be extracted !! "
		RequestedFields['branch_op']=1
		RequestedFields['int_op']=1
		RequestedFields['logic_op']=1
		RequestedFields['load_op']=1
		RequestedFields['store_op']=1
		RequestedFields['total_mem_op']=1		
		RequestedFields['total_mem_bytes']=1
		RequestedFields['dudist1']=1
		#RequestedFields['duint1']=1
		#RequestedFields['dufp1']=1
		#RequestedFields['dufp2']=1
		#RequestedFields['ducnt2']=1
		for CurrField in RequestedFields:
			print "\t "+str(CurrField)
	else:
		
		IpFile=open(FieldsFileName)
		ReadReqFields=IpFile.readlines()
		IpFile.close()
		
		for CurrLine in ReadReqFields:
			Tmp=RemoveWhiteSpace(CurrLine)
			if( Tmp!=''):
				RequestedFields[Tmp]=-1
				print "\t Requested Field "+str(Tmp)
	
	NumLinesPerBBStats=10
	print "\n\t Assuming that the format of BB stats is not changed and has "+str(NumLinesPerBBStats)+" lines in it ! "

	
	#OutStream.write("\n\t Format: <Blk-ID> Op1 Op2 Div \n\n");
	#OutStream.write("\n\t ---------------- Requested details/Working assumption ---------------- \n")
	#OutStream.write("\n\t NumLinesPerBBStats: "+str(NumLinesPerBBStats))
	SuitableBlks=0
	#RatioCoefficient=1.0
	IpFile=open(ListofFiles[0])
	ReadHeader=IpFile.readlines()
	IpFile.close()
	
	AllFieldsFound=0
	FieldsLineNum=-1
	FieldsLocation={}
	LineStartIdentifier={}
	SequenceNotFound=1
	

	LineIdentifierIdx=0
	LineNumIdx=1
	FieldNumIdx=2
	BBValuesStartLine=-1
	for LineNum,CurrLine in enumerate(ReadHeader):
			if( not(AllFieldsFound) ):
				if SequenceNotFound:
					CheckLine=re.match('\s*\#\s*\<sequence',CurrLine)
					if CheckLine:
						print "\n\t Apparently found sequence line on linenum "+str(LineNum)+" is it?? "+str(CurrLine)
						SequenceNotFound=0
						FieldsLineNum+=1
						BBValuesStartLine=LineNum+NumLinesPerBBStats
				else:
					CheckLine=re.match('\s*\#\s*\+(.*)',CurrLine)
					if CheckLine:
						#print "\n\t Rest of it: "+str(CheckLine.group(1))
						SplitFields=re.split('<',CheckLine.group(1))
						FieldsLineNum+=1
						CurrLineStartIdentifier=''
						for FieldNum,CurrField in enumerate(SplitFields):
							if FieldNum:
								CurrField=RemoveWhiteSpace(CurrField)
								Tmp=re.sub('\>(.*)$','',CurrField)
								#print "\n\t CurrField: "+str(CurrField)+" Tmp "+str(Tmp)
								Tmp=RemoveWhiteSpace(Tmp)
								FieldsLocation[Tmp]=(CurrLineStartIdentifier,FieldsLineNum,FieldNum)
							else:
								#print "\n\t LineStartIdentifier: "+str(CurrField)
								LineStartIdentifier[CurrField]=FieldsLineNum
								CurrLineStartIdentifier=CurrField
						if(FieldsLineNum==(NumLinesPerBBStats-1)):
							AllFieldsFound=1 #Although line num is zero indexed since start of header is precedded by identifier '<no additional info>' even that will be counted as a fields' line. Hence making this exception to compare a 0 and 1 index count.
						#else: 
							#print "\n\t AllFieldsFound: "+str(AllFieldsFound)+" NumLinesPerBBStats: "+str(NumLinesPerBBStats)+" str FieldsLineNum: "+str(FieldsLineNum)
					#sys.exit()
			else:
				break

	RequiredLines={}	
	print "\n\t -------------------------------------- "
	FieldsStr=''
	FieldsCollection=[]		
	for CurrField in RequestedFields:
		if( CurrField in FieldsLocation):
			if(CurrField!='dudist1'):
				FieldsStr+='\t'+str(CurrField)
				FieldsCollection.append(CurrField)
				#print "\n\t Field---- "+str(CurrField)
			CurrFieldsLine=FieldsLocation[CurrField][LineNumIdx]
			RequestedFields[CurrField]=FieldsLocation[CurrField]
			if(not(CurrFieldsLine in RequiredLines)):
				RequiredLines[CurrFieldsLine]=[]	
			RequiredLines[CurrFieldsLine].append(CurrField)
			print "\n\t Field: "+str(CurrField)+" is available in "+str(CurrFieldsLine)+" FieldNum: "+str(FieldsLocation[CurrField][FieldNumIdx])
		else:
			print "\n\t ERROR: Field "+str(CurrField)+" is not found in the header!! "
			sys.exit() 
			
	OutStream.write("\n\t Format: <File>\t <BB-ID>\t "+str(FieldsStr) );
	OutStream.write("\n\n\t\t ------------------------------------------------------------------\n\n")
	
	ExtractedStats={}
        for idx,CurrFile in enumerate(ListofFiles):
		IpFile=open(CurrFile)
		CurrStaticFile=IpFile.readlines()
		IpFile.close()
		InputLen=len(CurrStaticFile)	 
		ExtractedStats[CurrFile]={}
		LineNum=BBValuesStartLine

		FindBBs={}
		for CurrBB in ListofBBs:
			FindBBs[CurrBB]=0
		NumBBsNeeded=0
		NumBBsFound=0
		for CurrBB in FindBBs:
			NumBBsNeeded+=1
			 
		while(LineNum<InputLen):
		 CurrLine=CurrStaticFile[LineNum]
		 BBExtract=re.match("\s*.*\#(.*)",CurrStaticFile[LineNum])
		 if BBExtract:
		  BBphrase=re.split('\t',BBExtract.group(1))
		  BBNum=RemoveWhiteSpace(BBphrase[0])
		  print "\t LineNum: "+str(LineNum)
		  if(BBNum in FindBBs):
		  	print "\t BBNum: "+str(BBNum)
			print "\t LineNum: "+str(LineNum)
	   		FindBBs[BBNum]=1
		   	print "Yabadabbadooooo! \n\n"
			print "\n\t Is this the start-line: "+str(CurrStaticFile[LineNum])
			StartLineNum=(LineNum)
			ExtractedStats[CurrFile][BBNum]={}

			for CurrLineNum in RequiredLines:
				print "\n\t Need line: "+str(CurrLineNum)	
				CurrLine=CurrStaticFile[StartLineNum+CurrLineNum]
				CheckLine=re.match('\s*\+(.*)\s*\#',CurrLine)
				if CheckLine:
					RestOfLine=CheckLine.group(1)
					Breakdown=re.split('\t',RestOfLine)
					#print "\n\t Rest of it: "+str(RestOfLine)
					StartTerm=RemoveWhiteSpace(Breakdown[0])
					print "\t Num(Breakdown) "+str(len(Breakdown))+" Start-- "+str(StartTerm)
					if(StartTerm!='dud'):
					 for CurrField in RequiredLines[CurrLineNum]:
						FieldNum=RequestedFields[CurrField][FieldNumIdx]
						print "\t Field "+str(CurrField)+" "+str(Breakdown[FieldNum])
						ExtractedStats[CurrFile][BBNum][CurrField]=Breakdown[FieldNum]
					else:
					 ExtractedStats[CurrFile][BBNum]['dud']={}
					 TotalExprn=''
					 for Idx in range(1,len(Breakdown)):
					  	UseThisToBreakdown=Breakdown[Idx]
					  	if(Idx==(len(Breakdown)-1)):
					  		 UseThisToBreakdown=''
							 LastItemExtract=re.match('\s*(.*)\s*\#.*',Breakdown[len(Breakdown)-1])
							 if(LastItemExtract):
							 	LastItem=RemoveWhiteSpace(LastItemExtract.group(1))
							 	UseThisToBreakdown=LastItem
							 	#print "\t LastItem: "+str(LastItem)
						if(UseThisToBreakdown!=''):	 	 	
						   	TotalExprn+='\t'+UseThisToBreakdown
						 	MiniBreakdown=re.split(':',UseThisToBreakdown)
					 		if(len(MiniBreakdown)==3):
						 		dist=int(MiniBreakdown[0])
						 		ExtractedStats[CurrFile][BBNum]['dud'][dist]=(int(MiniBreakdown[1]),int(MiniBreakdown[2]))
						 		#print "\t Dud-term: "+str(UseThisToBreakdown)+' dist '+str(dist)+' mini-break '+str(ExtractedStats[CurrFile][BBExtract]['dud'][int(MiniBreakdown[0])])
						 	else:
						 		print "\t LineNum: "+str(StartLine+CurrLineNum)+" exprn: "+str(UseThisToBreakdown)+" does not have three fields seperated by ':', instead has "+str(len(MiniBreakdown))
						 		print "\t Currently this situation is handled as critical error!! "
						 		sys.exit()
						 		
					 		
					 print "\t TotalExprn: "+str(TotalExprn)
			NumBBsFound+=1
			#sys.exit()
		 if(NumBBsNeeded==NumBBsFound):
		 	LineNum=InputLen								
		 else:	
		 	LineNum+=NumLinesPerBBStats										
							

		for CurrBB in FindBBs:
			print "\t 1. What next ??"
			if(CurrBB in ExtractedStats[CurrFile]):
				AllFields=''
				for CurrField in FieldsCollection:
					if(CurrField in ExtractedStats[CurrFile][CurrBB]):
						if(CurrField!='dud'):
							AllFields+='\t'+str(ExtractedStats[CurrFile][CurrBB][CurrField])
							print "\t CurrField: "+str(CurrField)+"---"+str(ExtractedStats[CurrFile][CurrBB][CurrField])
				OutStream.write("\n\t "+str(CurrFile)+"\t "+str(CurrBB)+" "+str(AllFields))

	print "\t $$$$$ "				
	#OutStream.write("\n\n\t Found "+str(NumBlks)+" blocks of which "+str(SuitableBlks)+" blocks have ratio of "+str(RatioCoefficient))	
	#print("\n\n\t Found "+str(NumBlks)+" blocks of which "+str(SuitableBlks)+" blocks have ratio of "+str(RatioCoefficient))
	#OutStream.write("\n\n")
						
	

if __name__=="__main__":
	main(sys.argv[1:])

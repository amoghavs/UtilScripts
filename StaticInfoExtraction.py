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
           opts, args = getopt.getopt(sys.argv[1:],"i:b:f:h:d",["input","bb","fields","ratio","numfields","statnum","operand1","operand2","output","help","verbose"])
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
	   elif opt in ("-d","-debug"):
		debugStr=RemoveWhiteSpace(arg)
		debug=int(debugStr)
		print "\n\t Debug option is "+str(debug)
	   else:  
		usage()
		

	if( (SourceFile=='') ):
		usage()
		
	IpFile=open(SourceFile)
	Input=IpFile.readlines()
	IpFile.close()

	NumBlks=0
	InputLen=len(Input)

        ListofFiles=[] 
	for CurrLine in Input:
		Tmp=RemoveWhiteSpace(CurrLine)
		if(not(Tmp=='')):
			ListofFiles.append(Tmp)	       
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
		print "\n\t Fields file is not provided. Hence following fields will be extracted and provided!! "
		RequestedFields['branch_op']=1
		RequestedFields['int_op']=1
		RequestedFields['logic_op']=1
		RequestedFields['load_op']=1
		RequestedFields['store_op']=1
		RequestedFields['total_mem_op']=1		
		RequestedFields['total_mem_bytes']=1
		RequestedFields['dudist1']=1
		RequestedFields['duint1']=1
		RequestedFields['dufp1']=1
		RequestedFields['dufp2']=1
		RequestedFields['ducnt2']=1
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

	#OutStream.write("\n\t Format: <Blk-ID> Op1 Op2 Add Sub Mult Div \n\n");
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

	for LineNum,CurrLine in enumerate(ReadHeader):
			if( not(AllFieldsFound) ):
				if SequenceNotFound:
					CheckLine=re.match('\s*\#\s*\<sequence',CurrLine)
					if CheckLine:
						print "\n\t Apparently found sequence line on linenum "+str(LineNum)+" is it?? "+str(CurrLine)
						SequenceNotFound=0
						FieldsLineNum+=1
				else:
					CheckLine=re.match('\s*\#\s*\+(.*)',CurrLine)
					if CheckLine:
						print "\n\t Rest of it: "+str(CheckLine.group(1))
						SplitFields=re.split('<',CheckLine.group(1))
						FieldsLineNum+=1
						CurrLineStartIdentifier=''
						for FieldNum,CurrField in enumerate(SplitFields):
							if FieldNum:
								CurrField=RemoveWhiteSpace(CurrField)
								Tmp=re.sub('\>(.*)$','',CurrField)
								print "\n\t CurrField: "+str(CurrField)+" Tmp "+str(Tmp)
								Tmp=RemoveWhiteSpace(Tmp)
								FieldsLocation[Tmp]=(CurrLineStartIdentifier,FieldsLineNum,FieldNum)
							else:
								print "\n\t LineStartIdentifier: "+str(CurrField)
								LineStartIdentifier[CurrField]=FieldsLineNum
								CurrLineStartIdentifier=CurrField
						if(FieldsLineNum==(NumLinesPerBBStats-1)):
							AllFieldsFound=1 #Although line num is zero indexed since start of header is precedded by identifier '<no additional info>' even that will be counted as a fields' line. Hence making this exception to compare a 0 and 1 index count.
						else: 
							print "\n\t AllFieldsFound: "+str(AllFieldsFound)+" NumLinesPerBBStats: "+str(NumLinesPerBBStats)+" str FieldsLineNum: "+str(FieldsLineNum)
			else:
				break

	RequiredLines={}			
	for CurrField in RequestedFields:
		if( CurrField in FieldsLocation):
			CurrFieldsLine=FieldsLocation[CurrField][LineNumIdx]
			RequiredLines[CurrFieldsLine]=CurrFieldsLine
			print "\n\t Field: "+str(CurrField)+" is available in "+str(CurrFieldsLine)
		else:
			print "\n\t ERROR: Field "+str(CurrField)+" is not found in the header!! "
			sys.exit() 
			
	sys.exit()

        for idx,CurrFile in enumerate(ListofFiles):
	 IpFile=open(CurrFile)
	 CurrStaticFile=IpFile.readlines()
	 IpFile.close()
	 InputLen=len(CurrStaticFile)	 

	 for LineNum in range(InputLen):
		CurrLine=CurrStaticFile[LineNum]
		BlkLine=re.match('\s*\+vec.*',CurrLine)
		if BlkLine:
			NumBlks+=1
			BlockID=re.split('\t',BlkLine.group(0))
			#print "\n\t Found +vec at line number "+str(LineNum)
			FieldLine=LineNum+LineNumAdjust
			# Can actually loop over all the details/lines if needed! Can/Should adjust LineNumAdjust for that! 
			if(FieldLine):
				ReqFields=re.split('\t',CurrStaticFile[FieldLine])
				# First and last field is common/non-stat line, except maybe the first line! 
				if debug: 
					OutStream.write("\n\t Field line: "+str(CurrStaticFile[FieldLine]))
				if( (len(ReqFields)-2)== NumFields):				
					if debug:
						OutStream.write("\n\t So, I have "+str(len(ReqFields)-2)+" fields, it is equal to "+str(NumFields)+" !!")
					"""Op1=int(RemoveWhiteSpace(ReqFields[Operand1Idx]))
					Op2=int(RemoveWhiteSpace(ReqFields[Operand2Idx]))
					Add=Op1+Op2
					Sub=Op1-Op2
					Mult=Op1*Op2
					Div=0
					if(Op2):
						Div= float( Op1/Op2 )
					BBID=re.match('.*\#\s*0x(.*)',ReqFields[len(ReqFields)-1])
					#if( Div > RatioCoefficient):
					if( (Op1) and (Op1 > (Op2*RatioCoefficient))):
						SuitableBlks+=1
						""if BBID:
							OutStream.write("\n\t"+str(BBID.group(1))+"\t"+str(Op1)+"\t"+str(Op2)+"\t"+str(Add)+"\t"+str(Sub)+"\t"+str(Mult)+"\t"+str(Div))
						else:
							OutStream.write("\n\tN/A \t"+str(Op1)+"\t"+str(Op2)+"\t"+str(Add)+"\t"+str(Sub)+"\t"+str(Mult)+"\t"+str(Div))""
						if BBID:
							OutStream.write("\n\t"+str(BBID.group(1))+"\t"+str(Op1)+"\t"+str(Op2)+"\t"+str(Div))
						else:
							OutStream.write("\n\tNA\t"+str(Op1)+"\t"+str(Op2)+"\t"+str(Div))"""
				
				else:
					print "\n\t ERROR: (len(ReqFields)-2): "+str(len(ReqFields)-2)+" is not same as "+str(NumFields)+" ie., (len(ReqFields)-2)== NumFields is not met!! \n"
					sys.exit(0)

	OutStream.write("\n\n\t Found "+str(NumBlks)+" blocks of which "+str(SuitableBlks)+" blocks have ratio of "+str(RatioCoefficient))	
	print("\n\n\t Found "+str(NumBlks)+" blocks of which "+str(SuitableBlks)+" blocks have ratio of "+str(RatioCoefficient))
	OutStream.write("\n\n")
						
	

if __name__=="__main__":
	main(sys.argv[1:])

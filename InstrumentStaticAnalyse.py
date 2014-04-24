# /usr/bin/python 
import sys,re,getopt

def usage():
	print "\n\t InstrumentStaticAnalyse.py -i <static-file> -n Number-of-fields -s Stat-line-num -a Op1 index -b Op2 index. \n\t Optional inputs: -d <debug:default=0> -o <Output-file> "
	sys.exit()
def WhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output
	
def main(argv):
        SiminstFile=''
        debug=0
	OutFileName=''
	NumFields=''
	StatNum=''
	Operand1Idx=''
	Operand2Idx=''
	RatioCoefficient=''
        try:
           opts, args = getopt.getopt(sys.argv[1:],"i:r:n:s:a:b:o:h:d:v",["input","ratio","numfields","statnum","operand1","operand2","output","help","verbose"])
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
	   elif opt in ("-n","-numfields"):
		NumFieldsStr=WhiteSpace(arg)
		NumFields=int(NumFieldsStr)
		print "\n\t Number of fields is "+str(NumFields)
           elif opt in ("-r", "--ratio"):
           	RatioCoefficientStr=WhiteSpace(arg)
           	RatioCoefficient=float(RatioCoefficientStr)
           	print "\n\t RatioCoefficient: "+str(RatioCoefficient)   		
	   elif opt in ("-s","-statnum"):
		StatNumStr=WhiteSpace(arg)
		StatNum=int(StatNumStr)
		print "\n\t Number of fields is "+str(StatNum)
	   elif opt in ("-a","--operand1"):
		Operand1IdxStr=WhiteSpace(arg)
		Operand1Idx=int(Operand1IdxStr)
		print "\n\t Operand 1 is "+str(Operand1Idx)		
	   elif opt in ("-b","-operand2"):
		Operand2IdxStr=WhiteSpace(arg)
		Operand2Idx=int(Operand2IdxStr)
		print "\n\t Operand 1 is "+str(Operand2Idx)
	   elif opt in ("-d","-debug"):
		debugStr=WhiteSpace(arg)
		debug=int(debugStr)
		print "\n\t Debug option is "+str(debug)
           elif opt in ("-o","--output"):
           	OutFileName=WhiteSpace(arg)
           	print "\n\t Out file is "+str(OutFileName)	   
	   else:  
		usage()
		

	if( (SiminstFile=='') or (NumFields=='') or (StatNum=='') or (Operand1Idx=='') or (Operand2Idx=='') ):
		usage()
	if(RatioCoefficient==''):
		RatioCoefficient=1.0
		print "\n\t Assuming the ratio required is "+str(RatioCoefficient)+"\n"	
	if(OutFileName!=''):
		OutStream=open(OutFileName,'w')
	else:
		OutStream=sys.stdout
		
	Inp=open(SiminstFile)
	Input=Inp.readlines()
	NumBlks=0
	InputLen=len(Input)
	NumLinesPerBBStats=10
	LineNumAdjust=StatNum-NumLinesPerBBStats;
	print "\n\t Assuming that the format of BB stats is not changed and has "+str(NumLinesPerBBStats)+" lines in it ! "
	print "\n\t Will extract the "+str(StatNum)+" numbered(1-index) line in BB stats. It should be having "+str(NumFields)+" fields in it and the indices of Op1 and Op2 are assumed to be index-1 \n"

	#OutStream.write("\n\t Format: <Blk-ID> Op1 Op2 Add Sub Mult Div \n\n");
	OutStream.write("\n\t Format: <Blk-ID> Op1 Op2 Div \n\n");
	OutStream.write("\n\t ---------------- Requested details/Working assumption ---------------- \n")
	OutStream.write("\n\t NumLinesPerBBStats: "+str(NumLinesPerBBStats))
	OutStream.write("\n\t StatNum: "+str(StatNum))
	OutStream.write("\n\t NumFields: "+str(NumFields))
	OutStream.write("\n\t Op1: "+str(Operand1Idx)+" Op1: "+str(Operand2Idx)+"\n\n")
	SuitableBlks=0
	#RatioCoefficient=1.0 
	for LineNum in range(InputLen):
		CurrLine=Input[LineNum]
		BlkLine=re.match('\s*\+vec.*',CurrLine)
		if BlkLine:
			NumBlks+=1
			BlockID=re.split('\t',BlkLine.group(0))
			#print "\n\t Found +vec at line number "+str(LineNum)
			FieldLine=LineNum+LineNumAdjust
			# Can actually loop over all the details/lines if needed! Can/Should adjust LineNumAdjust for that! 
			if(FieldLine):
				ReqFields=re.split('\t',Input[FieldLine])
				# First and last field is common/non-stat line, except maybe the first line! 
				if debug: 
					OutStream.write("\n\t Field line: "+str(Input[FieldLine]))
				if( (len(ReqFields)-2)== NumFields):				
					if debug:
						OutStream.write("\n\t So, I have "+str(len(ReqFields)-2)+" fields, it is equal to "+str(NumFields)+" !!")
					Op1=int(WhiteSpace(ReqFields[Operand1Idx]))
					Op2=int(WhiteSpace(ReqFields[Operand2Idx]))
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
						"""if BBID:
							OutStream.write("\n\t"+str(BBID.group(1))+"\t"+str(Op1)+"\t"+str(Op2)+"\t"+str(Add)+"\t"+str(Sub)+"\t"+str(Mult)+"\t"+str(Div))
						else:
							OutStream.write("\n\tN/A \t"+str(Op1)+"\t"+str(Op2)+"\t"+str(Add)+"\t"+str(Sub)+"\t"+str(Mult)+"\t"+str(Div))"""
						if BBID:
							OutStream.write("\n\t"+str(BBID.group(1)))#+"\t"+str(Op1)+"\t"+str(Op2)+"\t"+str(Div))
						else:
							OutStream.write("\n\tNA\t"+str(Op1)+"\t"+str(Op2)+"\t"+str(Div))
				else:
					print "\n\t ERROR: (len(ReqFields)-2): "+str(len(ReqFields)-2)+" is not same as "+str(NumFields)+" ie., (len(ReqFields)-2)== NumFields is not met!! \n"
					sys.exit(0)

	OutStream.write("\n\n\t Found "+str(NumBlks)+" blocks of which "+str(SuitableBlks)+" blocks have ratio of "+str(RatioCoefficient))	
	print("\n\n\t Found "+str(NumBlks)+" blocks of which "+str(SuitableBlks)+" blocks have ratio of "+str(RatioCoefficient))
	OutStream.write("\n\n")
						
	

if __name__=="__main__":
	main(sys.argv[1:])

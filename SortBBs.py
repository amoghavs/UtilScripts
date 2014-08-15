
import sys,getopt,subprocess,re,math,commands,time,copy,random
from operator import itemgetter, attrgetter

def usage():
	print "\n\t Usage: SortBBs.py -i <input-file> optional: -o <output-file> \n"
	sys.exit()

def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output
	
def IsNumber(s):
# Credits: StackExchange: DanielGoldberg: http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
	try:
		float(s)
		return True
	except ValueError:
		return False

def main(argv):
	SrcFileName=''
	OutputFileName=''
	PercentThreshold=''
	try:
	   opts, args = getopt.getopt(sys.argv[1:],"i:o:p:h:v",["list","output","percent","help","verbose"])
	except getopt.GetoptError:
		#print str(err) # will print something like "option -a not recognized"
	   usage()
	   sys.exit(2)
	verbose=False   
	for opt, arg in opts:
	   print "\n\t Opt: "+str(opt)+" argument "+str(arg)	
	   if opt == '-h':
	      usage()
	   elif opt in ("-i", "--input"):
	      SrcFileName=arg
	      print "\n\t Source file is "+str(SrcFileName)+"\n";
	   elif opt in ("-o","--output"):
	      OutputFileName=arg
	      print "\n\t Output file name is "+str(OutputFileName)+"\n"
	   elif opt in ("-p","-percent"):
	   	Percent=float(RemoveWhiteSpace(arg))
	   	print "\n\t Percent is "+str(Percent)+"\n"
           else:
   		usage()

	if( (SrcFileName=='') or (OutputFileName=='') ):
		usage()
	if(PercentThreshold==''):
		PercentThreshold=0.5
	InFile=open(SrcFileName)
	BBFile=InFile.readlines()
	InFile.close()
	
	print "\n\t Num of lines: "+str(len(BBFile))
	BBIdx=0
	PercentIdx=1
	CollectTopLoopInfo=[]
	for LineNum,ExtractLine in enumerate(BBFile):
		#print "\n\t CurrLine: "+str(CurrLine)
		CurrLine=ExtractLine
		CurrLine=RemoveWhiteSpace(CurrLine)
		TopLoopCheck=ExtractLine.split('\t')
		Fields=CurrLine.split('\t')
		if(len(Fields)>4):
			#print "\n\t --LineNum: "+str(LineNum)+" #Fields "+str(len(Fields))
			print "\n\t CurrLine: "+str(CurrLine)
		else:
			if(len(TopLoopCheck)==5):
				#print "\n\t 
				TmpBB=Fields[BBIdx].split(':')
				BB=''
				Percent=RemoveWhiteSpace(Fields[PercentIdx])
				if(len(TmpBB)==2):
					BB=TmpBB[1]
				#print "\n\t Percent: "+str(float(Percent))
				CollectTopLoopInfo.append( (BB,float(Percent)) )

	CollectTopLoopInfo=sorted(CollectTopLoopInfo, key=itemgetter(PercentIdx),reverse=True)
	#for Idx,CurrBBTuple in enumerate(CollectTopLoopInfo):	
	#	print "\n\t BB: "+str(CurrBBTuple[BBIdx])+" Percent: "+str(CurrBBTuple[PercentIdx])

	OutputFile=open(OutputFileName,'w')
	
	for Idx,CurrBBTuple in enumerate(CollectTopLoopInfo):
		if(CurrBBTuple[PercentIdx] > PercentThreshold):
			OutputFile.write(str(CurrBBTuple[BBIdx])+"\n")
			print("\n\t "+str(CurrBBTuple[PercentIdx]))

if __name__ == "__main__":
   main(sys.argv[1:])
	
	
	
	
	
	
	
	
	

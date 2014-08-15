import sys,re,getopt,commands

def usage():
	print "\n\t PowerGovRun.py -t <sampling-period> -l <Source file with executables> \n\t Optional: \n\t\t -s <0:List has exes; 1: List has source(.c) files> "
	print "\n\t Run the script as root "
	sys.exit()
	
def RemoveWhiteSpace(Input):
	temp=re.sub('^\s*','',Input)
	Output=re.sub('\s*$','',temp)
	
	return Output


def main(argv):
        SamplingTime=''
        ListFile=''
        SourceFlag=''
        debug=0
        verbose=False
        try:
           opts, args = getopt.getopt(sys.argv[1:],"t:l:s:h:v",["sampling","list","source","help","verbose"])
        except getopt.GetoptError:
                #print str(err) # will print something like "option -a not recognized"
           usage()
           sys.exit(2)
        #verbose=False   
        for opt, arg in opts:
        	if opt == '-h':
        		usage()
        		sys.exit()
        	elif opt in ("-t", "--sampling"):
        		SamplingTime=int(RemoveWhiteSpace(arg))
        		print "\n\t  Sampling time is "+str(SamplingTime)
        	elif opt in ("-l", "--list"):
        		ListFile=RemoveWhiteSpace(arg)
        		print "\n\t Source file is "+str(ListFile)
        	elif opt in ("-s","--source"):
        		SourceFlag=int(RemoveWhiteSpace(arg))
        		print "\n\t SourceFlag is "+str(SourceFlag)
        	elif opt in ("-v","--verbose"):
        		verbose=False
	   	else:  
		usage()
	
	if( (SamplingTime=='') or (ListFile=='') ):
		usage()
	if(SourceFlag==''):
		SourceFlag=1
	ExeFile=open(ListFile)
	ExeSet=ExeFile.readlines()
	ExeFile.close()
	
	for CurrExe in ExeSet:
		if(CurrExe==''):
			if(SourceFlag):
				ExtractFileName=re.match('\s*(.*)\.c',ExeSet)
				if(ExtractFileName):
					ExeName=RemoveWhiteSpace(ExtractFileName.group(1))
			else:
				ExeName=RemoveWhiteSpace(ExeSet)
				
			if(ExeName):
				print "\n\t Attempting to run: "+str(ExeName)
				commands.getoutput('./'+str(ExeName))
				
			


if __name__=="__main__":
	main(sys.argv[1:])	

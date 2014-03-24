# /usr/bin/python 
import sys,re,getopt

def usage():
	print "\n\t ExtractCacheStats.py -i <siminst-file> "
	sys.exit()

def main(argv):
        SiminstFile=''
        debug=0
        try:
           opts, args = getopt.getopt(sys.argv[1:],"i:h:v",["config","deubg","help","verbose"])
        except getopt.GetoptError:
                #print str(err) # will print something like "option -a not recognized"
           usage()
           sys.exit(2)
        verbose=False   
        for opt, arg in opts:
           if opt == '-h':
              usage()
              sys.exit()
           elif opt in ("-i", "--config"):
              SiminstFile=arg
              print "\n\t Input file is "+str(SiminstFile)
	   else:  
		usage()
	Inp=open(SiminstFile)
	Input=Inp.readlines()

	NumLines=len(Input)	
	CacheStats={}
	for LineNum in range(0,len(Input)):
		CurrLine=Input[LineNum]
		SysIDLine=re.match('\s*.*sysid.*',CurrLine)
		if SysIDLine:
			print "\n\t Found a sysid at line "+str(LineNum)
			SysID=re.match('\s*.*sysid(\d+)*.*',CurrLine)
			if SysID:
				print "\n\t SysID being detected is "+str(SysID.group(1))
				CacheStats[SysID.group(1)]={}
				offset=1
				CurrSysID=SysID.group(1)
			for j in range(3):
				if( (j+LineNum) < (NumLines) ):
					CurrLine=Input[LineNum+j+offset]
					if (j<2):
						#print "\n\t Processing line: "+str
						CacheStatsLine=re.match('\s*.*l.*\[',CurrLine)
						if CacheStatsLine:
							print "\n\t CacheStatsLine: "+str(CacheStatsLine.group(0))
							Numbers=re.split('\[',CurrLine)
							if Numbers:
								for CurrNum in Numbers:
									GetStats=re.match('\s*(\d+)*\/(\d+)*',CurrNum)
									if GetStats:
										if(j==0):
											print "\n\t Hits--Total"+str(GetStats.group(2))+"\t"+str(GetStats.group(1)) 
										#CacheStats[CurrSysID]	
										elif(j==1):
											print "\n\t Loads--Total "+str(GetStats.group(2))+"\t"+str(GetStats.group(1)) 
					else:
						HybridCacheLine=re.match('\s*HybridCache',CurrLine)
						if HybridCacheLine:
							print "\n\t --*-- HybridLine: "+str(CurrLine)
							Numbers=re.split('\[',CurrLine)
							if Numbers:
								FieldNum=-1
								for CurrNum in Numbers:
									FieldNum+=1
									GetStats=re.match('\s*(\d+)*\/(\d+)*',CurrNum)
									if GetStats:
										if(FieldNum==1):
											print "\n\t --*--- Hits--Total"+str(GetStats.group(2))+"\t"+str(GetStats.group(1)) 
										else:
											print "\n\t --*--- Loads--Total"+str(GetStats.group(2))+"\t"+str(GetStats.group(1)) 
					
				
					

if __name__=="__main__":
	main(sys.argv[1:])

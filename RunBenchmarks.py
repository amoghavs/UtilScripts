
import sys,re,subprocess,commands,os,time

def FindPID(UName,Exe,Calling):
	PScmd='ps -u '+str(UName)+' | grep '+str(Exe)
        duh=commands.getoutput(PScmd)
        print "\n\t --"+str(Calling)+"-- \t PScmd: "+str(PScmd)+" duh: " +str(duh)
	if duh:
		print "\n\t --"+str(Calling)+"-- \t This is where I am searching PID: "+str(duh)
		PID=re.match('\s*(\d+)*\s*.*',duh)
	        if PID:
        	        #print "\n\t Duh: "+str(duh)+" PID: "+PID.group(1)	
			return PID.group(1)
		else:
			return -1
	else:
		return -1

def main():
	print "\n\t Script to launch benchmarks and obtain their memory footprint through ps_mem.py script, assuming that the script is available as an executable in your home folder. Ohh yeah, make sure you are running as sudo \n"
	Benchmarks=["ft","mg"];
	CLASS=["A","B"]
	SummaryFileName='SummaryMemFootprint.log'
	LogFile=open(SummaryFileName,'w')
	UName=commands.getoutput('whoami')
	print "\n\t UName: "+str(UName)
	LogFile.close()
	for CurrBench in Benchmarks:
		for CurrClass in CLASS:
			Exe=CurrBench+'.'+CurrClass
			ExeLog=str(Exe)+'.log'
			RunExe='./bin/'+str(Exe)+' > '+str(ExeLog)
			print "\n\t --Parent-- \t Forking begins"
			ExeForkPID=os.fork()
			if ExeForkPID==0:
				commands.getoutput(RunExe)
				sys.exit(0)
			else:
				PIDExe=FindPID(UName,Exe,'Parent')
				print "\n\t --Parent-- \t Running "+str(Exe)+" with CMD "+str(RunExe)+" PID "+str(PIDExe)
				if(PIDExe):
					PsLog='PsMem_'+str(Exe)+'.log'
					RunPsMem='sudo ~/ps_mem.py -p '+str(PIDExe)+' -w 1 > '+str(PsLog)
					print"\n\t --Parent-- \t This is the Psmem run command: "+str(RunPsMem)
					PsForkPID=os.fork()
					if PsForkPID==0:
						print "\n\t --PsMem Child-- \t Hello from the thread launching ps_mem.py! \n"
						DUH=commands.getoutput(RunPsMem)
						if DUH:
							print "\n\t DUH-- "+str(DUH)
						print"\n\t --PsMem Child-- I am all done, exitting now!! \n"
						sys.exit(0)
					else:
						time.sleep(1)
						PsPID=FindPID('root','ps_mem.py','Parent')
						os.waitpid(ExeForkPID, 0) 
						print "\n\t --Parent-- \t Must have been done with running the benchmark and now should kill ps_mem.py with PID "+str(PsPID)
						time.sleep(1)
						if(PsPID!=-1):
							StopPsMem='sudo kill -9 '+PsPID
							print"\n\t --Parent-- \t This is my StopPsMem cmd: "+str(StopPsMem)
							time.sleep(3)
							commands.getoutput(StopPsMem)
							GrepRunTime='grep Time '+str(ExeLog)
							RunTimeGrepOutput=commands.getoutput(GrepRunTime)
							RunTimeExe=re.match('\s*Time\s*in\s*seconds\s*\=\s*(\d+)*.(\d+)*',RunTimeGrepOutput)
							print "\n\t --Parent-- \t Must have exited from all children threads by now! "
							print "\n\t RunTimeGrepOutput "+str(RunTimeGrepOutput)
							if RunTimeExe:
								StoreRunTime=str(RunTimeExe.group(1))+'.'+str(RunTimeExe.group(2))
								print "\n\t Runtime: "+str(StoreRunTime)
								LogFile=open(SummaryFileName,'a')
								LogFile.write("\n\t ^ Exe: "+str(Exe)+" runtime: "+str(StoreRunTime)+" ")
								LogFile.close()
								#print"\n Exe: "+str(Exe)+" runtime: "+str(StoreRunTime)
							else:
								print "\n\t WARNING: Unable to determine the runtime for the exe"+str(Exe)
							GrepMemFile='GrepMem.log'
							GrepMemUsed='grep \= '+str(PsLog)+' > '+str(GrepMemFile)
							MemUsedGrepOutput=commands.getoutput(GrepMemUsed)
							ReadGrepMemFile=open(GrepMemFile,'r')
							GrepMemLines=ReadGrepMemFile.readlines()
							ReadGrepMemFile.close()
							RecordedData={}
							for CurrLine in GrepMemLines:
								dummy=re.split('=',CurrLine) #print "\n\t The Grep Output for MemUsed is "+str(MemUsedGrepOutput)		
								FindRHS=re.match('\s*(\d+)*\.(\d+)*(.*)\s*$',dummy[1])
								if FindRHS:
									MemSize=str(FindRHS.group(1))+'.'+str(FindRHS.group(2))
									if (~( 1&(MemSize in RecordedData)) ):
										RecordedData[MemSize]=str(MemSize)+str(FindRHS.group(3))
										#print "\n\t MemSize: "+str(MemSize)
							LogFile=open(SummaryFileName,'a')
							for keys in RecordedData:	
								LogFile.write("\n\t $ Exe: "+str(Exe)+" Memsize: "+str(RecordedData[keys])+" ")
								#print "\n Exe: "+str(Exe)+" Memsize: "+str(RecordedData[keys])
							LogFile.close()
									
						else:
							print "\n\t --Parent-- \t Likely error with determining which process is running PsMem. Although not fatal, exitting from the script "

#	print "\n\t If you are running top, this is the PID: "+str(FindPID(UName,'top','Parent'))
	
	LogFile.close()			

if __name__=="__main__":
	main()
	print "\n"

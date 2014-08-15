#include<stdio.h>
#include<stdlib.h>
#include <time.h>
#include <sys/time.h>

int main(int argc,char*argv[])
{

	if(argc<2)
	{
		printf("\n\t ERROR: Expected arguments: \n\t\t 1. Size of array \n\n");
		exit(-1);
	}
	int Size=atoi(argv[1]);
	int i=0;
	int *A,*ToFlag;
	
	A=malloc(Size*sizeof(int));
	ToFlag=calloc(Size,sizeof(int));

	int Count=0;
	int Node=0;
	int JumpTo;

	while(Count< (Size-1))
	{
		JumpTo=(int)(rand()%Size);
		printf("\n\t Count: %d Node: %d whose from trying to reach to %d whose toflag is %d ",Count,Node,JumpTo,ToFlag[JumpTo]);
		
		if( (ToFlag[JumpTo]==0 ) ) //&& ( FromFlag[JumpTo]==0) )
		{
			Count++;
			A[Node]=JumpTo;
			ToFlag[JumpTo]++;
			ToFlag[Node]++;
			printf("\n\t Node: %d A[Node]: %d JumpTo: %d ToFlag[Jumpto]: %d ",Node,A[Node],JumpTo,ToFlag[JumpTo]);
			Node=JumpTo;
		}
			

	}
	A[Node]=0;
	long int Sum=0;
	for(i=0;i<Size;i++)
	{
		printf("\n\t i: %d A[i]: %d ",i,A[i]);
		Sum+=A[i];
	}
	printf("\n\t Sum: %ld \n\n",Sum);
return 0;

}

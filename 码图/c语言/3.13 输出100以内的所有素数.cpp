#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
	
	bool f = true;
	for (int i = 2; i <= 100; i++) 
	{
		f = true;
		for (int j = 2; j <=sqrt(double(i)); j++)
		{
			if (i % j == 0)
				f = false;

		}
		if (i<=3 || f)
			printf("%d,", i);
	}



}
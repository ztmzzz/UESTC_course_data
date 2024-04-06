#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
	int a;
	if (scanf("%d", &a) != 1 || a <= 3)
	{
		printf("error");
		return 0;
	}
	    
	for (int i = 2; i < sqrt(double(a)); i++) {
		if (a % i == 0) {
			printf("no");
			return 0;
		}
	}
	printf("yes");
}
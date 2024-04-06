#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
	int i=0,n,x,c,l=1,r,flag=0,temp=0;
	scanf("%d", &n);
	int a[100] = { 0 };
	getchar();
	while ((c = getchar()) != '\n')
	{
		if (c == ',')
		{
			a[i] = temp;
			i++;
			temp = 0;
			flag = 0;
		}
		else
		{
			flag = 1;
			temp = temp * 10 + (c - 48); 
		}
	}
	if (flag==1)
	{
		a[i] = temp;
	}
	scanf("%d", &x);
	r = n;
	i = (l + r) / 2;
	while (a[i] != x)
	{
		i = (l + r) / 2;
		if (a[i] == x)
		{
			printf("%d", i + 1);
			return 0;
		}
		else if (a[i] < x)
			l = i + 1;
		else r = i - 1;
	
			
	}
}
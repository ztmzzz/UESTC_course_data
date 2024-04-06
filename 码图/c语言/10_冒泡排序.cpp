#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
	int b[10],temp;
	for (int i = 0; i < 10; i++)
	{
		scanf("%d", &b[i]);
	}
	for (int i = 0; i < 10; i++)
	{
		for (int j = 0; j < 9-i; j++)
		{
			if (b[j] > b[j + 1])
			{
				temp = b[j];
				b[j] = b[j + 1];
				b[j + 1] = temp;
			}
		}
	}
	for (int i = 0; i < 9; i++) //循环输出排序以后的结果
	{
		printf("%d,", b[i]);
	}
	printf("%d", b[9]);

}
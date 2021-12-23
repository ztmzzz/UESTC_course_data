#include <stdio.h>
void main()
{
	char a[256];
	gets_s(a);
	int sum = 0,flag=1;
	for (int i = 0; a[i] != '\0'; i++) {
		if (a[i] == ' ')
			flag = 1;
		else if (flag == 1)
		{
			flag = 0;
			sum++;
		}
		

	}
	printf("%d", sum);
}
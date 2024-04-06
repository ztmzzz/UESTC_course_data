#include <stdio.h>
void main()
{
	char A[100];
	char* a = A;
	char B[100];
	char* b = B;
	int i = 0;
	gets_s(A);
	while (1)
	{
		*b++ = *a++;
		i++;
		if (*a == '\0')
			break;
		if (i == 2)
		{
			*b = '*';
			b++;
			i = 0;
		}
	}
	*b = '\0';
	printf("%s\n", B);
}
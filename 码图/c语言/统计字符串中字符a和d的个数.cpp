
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
	
	char s[1000];
	gets_s(s);
	int a = 0, b = 0;
	for (int i = 0; i <= _mbstrlen(s); i++) {
		if (s[i] == 'a')
			a++;
		if (s[i] == 'd')
			b++;
		}
	printf("a:%d,d:%d",a,b);

}
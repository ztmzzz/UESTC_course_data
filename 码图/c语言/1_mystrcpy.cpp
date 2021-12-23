#include <stdio.h>
void my_strcpy(char* destination, char* source) {
	if (destination == NULL || source == NULL)
	{
		printf("error\n");
		return;
	}
while(*source!=' ')
{
*destination=*source;
destination++;
source++;
}
*destination=*source;
}
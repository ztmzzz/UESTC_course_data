#include <stdio.h>
#include <malloc.h>
void swap(int* a, int* b)
{
	int temp = *a;
	*a = *b;
	*b = temp;
}
int main()
{
	int n;
	scanf("%d", &n);
	int* p = (int*)malloc(n * sizeof(int));
	for (int i = 0; i < n; i++) {
		scanf("%d", p + i);
	}
	for (int i = 0; i < n - 1; i++)
	{
		int min = i;
		for (int j = i + 1; j < n; j++)     
			if (*(p+j) < *(p+min))   
				min = j;   
		swap(p+min, p+i);   
	}
	for (int i = 0; i < n; i++) {
		printf("%d", *(p + i));
		if (i != n - 1)
			printf(",");
	}
	free(p);
}

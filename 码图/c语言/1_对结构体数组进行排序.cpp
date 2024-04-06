#include <stdio.h>
struct Person {
	int no;
	int age;
	int height;
};
void sort(Person* array, int n) {
	if (array == NULL || n<=0)
		printf("error");
	int min;
	int j;
	struct Person temp;
	for (int i = 0; i < n - 1; i++) {
		min = i;
		for (j = i + 1; j < n; j++) {
			if ((array + j)->no == (array + min)->no) {
				if ((array + j)->age == (array + min)->age) {
					if ((array + j)->height < (array + min)->height)
						min = j;
				}
				else if ((array + j)->age < (array + min)->age)
					min = j;
			}
			else if ((array + j)->no < (array + min)->no)
				min = j;
		}
		temp = *(array + i); *(array + i) = *(array + min); *(array + min) = temp;
	}
	}
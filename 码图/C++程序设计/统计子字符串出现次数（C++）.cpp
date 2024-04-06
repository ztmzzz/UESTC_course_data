#include <iostream>
using namespace std;
int SubStrNum(char* str, char* substr) {
	int i = 0, j, sum = 0,k;
	while (str[i] != '\0') {
		if (str[i++] == substr[0]) {
			j = 0;
			sum++;
			k = i;
			i--;
			while (substr[j] != '\0')
			{
				if (substr[j++] != str[i++]) {
					sum--;
					i = k;
					break;
				}
			}
		}
	}
	cout << "match times=" << sum;
	return 0;
}
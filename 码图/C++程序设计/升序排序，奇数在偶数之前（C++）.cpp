#include <iostream>
#include <limits>
using namespace std;
int main() {
	int a[10];
	int t,s=9;
	for (int i = 0; i < 10; i++) {
		cin >> t;
		if (t < 0) {
			s = i-1;
			break;
		}
		a[i] = t;
	}
	for (int i = 0; i < s; i++) {
		for (int j = 0; j < s - i; j++) {
			if (a[j] > a[j + 1]) {
				t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
			}
		}
	}
	for (int i = 0; i < s+1; i++) {
		if (a[i] % 2 == 1)
			cout << a[i] << ' ';
	}
	for (int i = 0; i < s+1; i++) {
		if (a[i] % 2 == 0)
			cout << a[i] << ' ';
	}
	return 0;
}

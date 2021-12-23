#include <iostream>
#include <limits>
using namespace std;
int main() {
	int n,sum=1;
	cin >> n;
	if (n < 1 || n>80 || n % 2 == 0) {
		cout << "error";
		return 0;
	}
	for (int i = n; i > 0; i -= 2) {
		for (int j = 0; j < (n - i) / 2; j++)
			cout << ' ';
		for (int j = 0; j < i; j++)
			cout << '*';
		cout << '\n';
	}
	return 1;
}

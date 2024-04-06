#include <iostream>
#include <limits>
using namespace std;
int main() {
	int n,sum=1;
	cin >> n;
	for (int i = 2; i <= n; i++) {
		if (INT_MAX / i <= sum) {
			cout << i-1 << "!=" << sum << endl;
			return 0;
		}
		sum *= i;
	}
	cout << n << "!=" << sum << endl;
}
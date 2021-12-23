#include <iostream>
#include <limits>
using namespace std;
int main() {
	int y,m;
	cin >> y >> m;
	m = m % 12;
	if ((y % 400 == 0 || y % 4 == 0 && y % 100 != 0) && m == 2) {
		cout << "days:29";
		return 0;
	}
	if (m == 2)
		cout << "days:28";
	else if (m == 4 || m == 6 || m == 9 || m == 11)
		cout << "days:30";
	else
		cout << "days:31";
	return 0;
}

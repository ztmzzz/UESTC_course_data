#include <iostream>
using namespace std;
void Matrix_Mul(int a[3][2], int b[2][4]) {
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 4; j++) {
			cout << a[i][0] * b[0][j] + a[i][1] * b[1][j] << ' ';
		}
		cout << endl;
	}
}


#include <stdio.h>
#include <malloc.h>
#include <iostream>
#include <math.h>
using namespace std;
unsigned long long m[600][600] = { 0 }; unsigned long long s[600][600] = { 0 };
void find(int i, int j,int out[]) {
	static int cou = 1;
	if (i == j) {
		out[cou++] = i;
	}
	else {
		out[cou++]= -1;
		find(i, s[i][j],out);
		find(s[i][j]+1, j,out);
		out[cou++]=-2;
	}
}
void solve(int n, int p[], int out[]) {

	for (int i = 1; i <= n; i++) {
		m[i][i] = 0;
	}
	for (int r = 2; r <= n; r++) {//iÓëjµÄ²îÖµ
		for (int i = 1; i <= n - r + 1; i++) {
			int j = i + r - 1;
			m[i][j] = (unsigned long long)(m[i + 1][j] + p[i - 1] * p[i] * p[j]);
			s[i][j] = (unsigned long long)i;
			for (int k = i + 1; k < j; k++) {
				unsigned long long t = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
				if (t < m[i][j]) {
					m[i][j] = t;
					s[i][j] = k;
				}
			}
		}
	}
	find(1, n,out);
	out[0] = m[1][n] % 1000000007;
}
#include <iostream>
using namespace std;

template <typename T1, typename T2> T1 get_sum(T1* a, T2 n) { 	T1 sum=0; 	for (int i = 0; i < n; i++) { 		sum += a[i]; 	} 	return sum; }

int main()
{
	int arr_int[6] = { 1, 2, 3, 4, 5, 6 };
	double arr_double[6] = { 1.1, 2.2, 3.3, 4.4, 5.5, 6.6 };
	cout << get_sum(arr_int, 6) << endl;
	cout << get_sum(arr_double, 6) << endl;
	return 0;
}

#include <iostream>
#include <string>
#include <math.h>
using namespace std;
#include "CDate.h"
Date::Date(int y , int m, int d ) {
	year = y; month = m; day = d;
	if (month > 12 || month < 1) {
		cout << "Invalid month!" << endl;
		month = 1;
	}
	if (day > days(year, month) || day < 1) {
		cout << "Invalid day!" << endl;
		day = 1;
	}
}
int  Date::days(int year, int month) {
	int m[] = { 31,28,31,30,31,30,31,31,30,31,30,31 };
	if (month != 2)
		return m[month - 1];
	else if ((year % 4 == 0) && (year % 100 != 0) || (year % 400 == 0))
		return 29;
	else
		return 28;
}
void Date::NewDay() {
	day++;
	if (day > days(year, month)) {
		day = 1;
		month++;
		if (month > 12) {
			month = 1;
			year++;
		}
	}
}
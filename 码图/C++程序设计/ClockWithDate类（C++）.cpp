#include <iostream>
using namespace std;
#include "ClockAndDate.h"
#define PI 3.14

int Date::days(int year, int month) {
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
class ClockWithDate :public Date, public Clock {
public:
	virtual void showTime() {
		Clock::showTime();
		Date::display();
	}
	virtual void run() {
		if (getSecond() == 59 && getMinute() == 59 && getHour() == 23) {
			NewDay();
		}
		Clock::run();
	}
	ClockWithDate(int h, int m, int s, int y, int mo, int d=1):Clock(h,m,s),Date(y,mo,d){}
};
Clock* Clock::createClockWithDate(int h, int m, int s, int year, int month, int day) {
	return new ClockWithDate(h, m, s, year, month, day);
}
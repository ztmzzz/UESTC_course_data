#include <iostream>
using namespace std;
#include "Clock.h"
#define PI 3.14

class NewClock :public Clock {
public:
	virtual void showTime() {
		if (getHour() > 11) {
			cout << "Now:" << getHour()-12 << ":" << getMinute() << ":" << getSecond() << "PM"<<endl;
		}
		else{
			cout << "Now:" << getHour() << ":" << getMinute() << ":" << getSecond() << "AM" << endl;
		}
	}
	NewClock(int h,int m,int s):Clock(h,m,s){}
};
Clock* Clock::createNewClock(int h, int m, int s) {
	return new NewClock(h, m, s);
}
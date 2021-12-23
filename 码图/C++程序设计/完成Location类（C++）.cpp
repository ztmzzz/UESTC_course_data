#include <iostream>
using namespace std;
#include "Location.h"
#define PI 3.14

Location& Location::operator +(Location& offset) {
	x = x + offset.x;
	y = y + offset.y;
	return *this;
}
Location& Location::operator -(Location& offset) {
	x = x - offset.x;
	y = y - offset.y;
	return *this;
}
#include <iostream>
#include <string>
#include <math.h>
using namespace std;
class Point {
private:
	double x, y;
public:
	double Distance(const Point &);
	Point(double, double);
};
double Point::Distance(const Point &p) {
	return sqrt(pow((x - p.x), 2) + pow((y - p.y), 2));
}
Point::Point(double a, double b) {
	x = a; y = b;
}
int main() {
	double a, b, c, d;
	cin >> a >> b >> c >> d;
	Point A(a, b), B(c, d);
	cout << A.Distance(B) << endl;
	return 0;
}
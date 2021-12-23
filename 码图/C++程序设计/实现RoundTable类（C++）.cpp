#include <iostream>
using namespace std;

#define PI 3.14

class Table {
private:
	float high;
public:
	float GetHigh() { return high; }
	Table(float a) { high = a; }
};
class Circle {
private:
	float radius;
public:
	float GetArea() { return radius* radius*PI; }
	Circle(float a) { radius = a; }
};
class RoundTable :public Table, public Circle {
private:
	char color[20];
public:
	char* GetColor() { return color; }
	RoundTable(float a, float b, char* c) :Table(b) , Circle(a) {
		strcpy(color, c);
	}
};
int main() {
	float radius, high;
	char color[20];
	cin >> radius >> high >> color;

	RoundTable RT(radius, high, color);
	cout << "Area:" << RT.GetArea() << endl;
	cout << "High:" << RT.GetHigh() << endl;
	cout << "Color:" << RT.GetColor() << endl;
	return 0;
}

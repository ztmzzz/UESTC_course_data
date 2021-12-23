#include <iostream>
using namespace std;
#include "Shape.h"
#define PI 3.14

class Rectangle :public Shape {
private:
	double l, w;
public:
	Rectangle(double l, double w) {
		this->l = l;
		this->w = w;
	}
	double GetArea() {
		return l * w;
	}
	double GetPerimeter() {
		return 2 * (l + w);
	}
};
class Circle :public Shape {
private:
	double r;
public:
	Circle(double r) {
		this->r = r;
	}
	double GetArea() {
		return PI*r*r;
	}
	double GetPerimeter() {
		return 2 * PI * r;
	}
};
Shape* Shape::createRectangle(double l, double w) { return new Rectangle(l, w); }
Shape* Shape::createCircle(double r) { return new Circle(r); }
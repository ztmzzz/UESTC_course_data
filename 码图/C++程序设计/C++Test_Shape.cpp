#include <iostream>
using namespace std;
#include "ShapeFactory.h"
#define PI 3.14
class Triangle :public ShapeFactory {
public:
	Triangle(float aa, float bb, float cc) {
		a = aa; b = bb; c = cc;
	}
	float Circumstance() {
		return a + b + c;
	}
private:
	float a, b, c;
 };

class Quadrilateral :public ShapeFactory {
public:
	Quadrilateral(float aa, float bb, float cc,float dd) {
		a = aa; b = bb; c = cc; d = dd;
	}
	float Circumstance() {
		return a + b + c+d;
	}
private:
	float a, b, c,d;
};
class Circle :public ShapeFactory {
public:
	Circle(float r) {
		a = r;
	}
	float Circumstance() {
		return a*2*PI;
	}
private:
	float a;
};

ShapeFactory* ShapeFactory::Create(float a, float b, float c) {
	ShapeFactory* p = new Triangle(a, b, c);
	return p;
}
ShapeFactory* ShapeFactory::Create(float a, float b, float c, float d) {
	ShapeFactory* p = new Quadrilateral(a, b, c,d);
	return p;
}
ShapeFactory* ShapeFactory::Create(float r) {
	ShapeFactory* p = new Circle(r);
	return p;
}
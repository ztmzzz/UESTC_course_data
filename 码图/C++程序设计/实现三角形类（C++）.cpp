#include <iostream>
#include <string>
#include <math.h>
using namespace std;
class Ctriangle {
private:
	double a, b, c;
public:
	void display();
	double GetPerimeter();
	double GetArea();
	Ctriangle(double,double,double);
};
Ctriangle::Ctriangle(double a , double b, double c) {
	Ctriangle::a = a;
	Ctriangle::b = b;
	Ctriangle::c = c;
}
void Ctriangle::display() {
	cout << "Ctriangle:a=" << a << ",b=" << b << ",c=" << c << endl;
}
double Ctriangle::GetPerimeter() {
	return a + b + c;
}
double Ctriangle::GetArea() {
	double p = GetPerimeter() / 2;
	return sqrt(p * (p - a) * (p - b) * (p - c));
}
int main() {
	double a, b, c;
	cin >> a >> b >> c;
	Ctriangle T(a, b, c);
	T.display();
	cout << "Perimeter:" << T.GetPerimeter() << endl;
	cout << "Area:" << T.GetArea() << endl;
	return 0;
}
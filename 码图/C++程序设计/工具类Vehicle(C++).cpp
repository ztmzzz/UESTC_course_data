#include <iostream>
using namespace std;
#include "Vehicle.h"
#define PI 3.14

class Car :public Vehicle {
public:
	Car(){ cout << "Car constructor..." << endl; }
	virtual void display() const {
		cout << "This is a car!" << endl;
	}
	~Car() {
		cout << "Car destructor..." << endl;
	}
};
class Truck :public Vehicle {
public:
	Truck() { cout << "Truck constructor..." << endl; }
	virtual void display() const {
		cout << "This is a truck!" << endl;
	}
	~Truck() {
		cout << "Truck destructor..." << endl;
	}
};
class Boat :public Vehicle {
public:
	Boat() { cout << "Boat constructor..." << endl; }
	virtual void display() const {
		cout << "This is a boat!" << endl;
	}
	~Boat() {
		cout << "Boat destructor..." << endl;
	}
};
Vehicle* Vehicle::createCar() { return new Car(); }
Vehicle* Vehicle::createTruck() { return new Truck(); }
Vehicle* Vehicle::createBoat() { return new Boat(); }
#include <iostream>
using namespace std;
#include "CNumberFactory.h"
#define PI 3.14
class CNumber :public CNumberFactory {
private:
	int a;
public:
	virtual void Add(int number) {
		a += number;
	};
	virtual void Sub(int number) {
		a -= number;
	};
	virtual int GetValue() { return a; };

	virtual void SetValue(int number) {
		a = number;
	};
};
CNumberFactory* CNumberFactory::Create()
{
	return new CNumber();
}

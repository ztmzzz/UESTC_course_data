#include <iostream> 


using namespace std;

class Date {
public:
	Date(int y = 1996, int m = 1, int d = 1) {
		day = d;
		month = m;
		year = y;
		if (m > 12 || m < 1)
		{
			month = 1;
		}
		if (d > days(y, m))
		{
			cout << "Invalid day!" << endl;
			day = 1;
		}
	};
	int days(int year, int month) {
		int m[] = { 31,28,31,30,31,30,31,31,30,31,30,31 };
		if (month != 2)
			return m[month - 1];
		else if ((year % 4 == 0) && (year % 100 != 0) || (year % 400 == 0))
			return 29;
		else
			return 28;
	};
	void display() {
		cout << year << "-" << month << "-" << day << endl;
	}
	friend ostream& operator << (ostream& , Date& );
	
private:
	int year;
	int month;
	int day;
};
ostream& operator << (ostream& out, Date& d) {
	out << d.year << "-" << d.month << "-" << d.day << endl;
	return out;
}



int main() {
	int y, m, d;
	cin >> y >> m >> d;
	Date dt(y, m, d);
	cout << dt;
	return 0;
}
#include <iostream>
#include <string>
#include <math.h>
using namespace std;
 int a1, a2, a3;
 int sum;
class Student {
private:
	int grade1, grade2, grade3;
	char* name;
	char* num;

public:
	Student(char*, char*, int, int, int);
	void display();
	double average1();
	double average2();
	double average3();
};

Student::Student(char* n, char* m, int a, int b, int c) {
	name = m;
	num = n;
	grade1 = a; grade2 = b; grade3 = c;
	a1 += a; a2 += b; a3 += c;
	sum++;
}
void Student::display() {
	cout << num << " " << name << " " << grade1 << " " << grade2 << " " << grade3 << endl;
}
double Student::average1(){
	return (double)a1 / sum;
}
double Student::average2() {
	return (double)a2 / sum;
}
double Student::average3() {
	return (double)a3 / sum;
}
int main() {
	Student* stu1, * stu2, * stu3;
	char name1[10], name2[10], name3[10];
	char num1[12], num2[12], num3[12];
	int grade1[3], grade2[3], grade3[3];
	cin >> name1 >> num1 >> grade1[0] >> grade1[1] >> grade1[2];
	cin >> name2 >> num2 >> grade2[0] >> grade2[1] >> grade2[2];
	cin >> name3 >> num3 >> grade3[0] >> grade3[1] >> grade3[2];
	stu1 = new Student(name1, num1, grade1[0], grade1[1], grade1[2]);
	stu2 = new Student(name2, num2, grade2[0], grade2[1], grade2[2]);
	stu3 = new Student(name3, num3, grade3[0], grade3[1], grade3[2]);

	stu1->display();
	stu2->display();
	stu3->display();

	cout << "The average grade of course1:" << stu2->average1() << endl;
	cout << "The average grade of course2:" << stu2->average2() << endl;
	cout << "The average grade of course3:" << stu2->average3() << endl;
	return 0;
}
#include <iostream>
#include <string>
#include <math.h>
using namespace std;
class User {
private:
	char *name[10];
	char *pass[10];
	int num;
public:
	void AddUser(const char*, const char*);
	int login(const char*, const char*);
	User(const char*, const char*);
};
User::User(const char* name, const char* pass) {
	num = 0;
	AddUser(name, pass);
}
void User::AddUser(const char* name, const char* pass) {
	User::name[num] = (char*)name;
	User::pass[num] = (char*)pass;
	num++;
}
int User::login(const char* name, const char* pass) {
	for (size_t i = 0; i < num; i++)
	{
		if (strcmp(name, User::name[i]) == 0) {
			if (strcmp(pass, User::pass[i]) == 0)
				return 1;
			else
				return -1;
		}
	}
	return -1;
}
int main() {
	char name[10], name1[10], pass[10], pass1[10];
	cin >> name >> pass >> name1 >> pass1;
	User user("LiWei", "liwei101");
	user.AddUser(name, pass);
	if (user.login(name1, pass1) >= 0)
	{
		cout << "Success Login!" << endl;
	}
	else {
		cout << "Login failed!" << endl;
	}
	return 0;
}
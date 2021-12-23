#include <iostream>
#include <string>
using namespace std;

int main() {
	string s1;
	string s2;
	string t;
	cin >> s1 >> s2;
	if (s1 == s2) {
		cout << 0;
		return 0;
	}
	if (s1.length() > s2.length()|| s1.length() == s2.length()&&s1>s2) {
		cout << '+';
		s2 = string(s1.length() - s2.length(), '0') + s2;
		t = s1;
	}
	else
	{
		cout << '-';
		s1 = string(s2.length() - s1.length(), '0') + s1;
		t = s1; s1 = s2; s2 = t;
	}
	for (int i = s1.length(); i >=0; i--) {
		if (s1[i] >= s2[i]) 
			t[i] = s1[i] - s2[i] + '0';
		else
		{
			t[i] = s1[i] - s2[i] + '9' + 1;
			s1[i - 1]--;
		}

		
	}
	cout << t;
	return 0;
}

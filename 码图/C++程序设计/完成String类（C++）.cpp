#include <iostream>
#include <string>
#include <math.h>
using namespace std;
#include "CString.h"
bool String::IsSubstring(const char* str) {
	for (int i = 0; i < len; i++) {
		if (mystr[i] == str[0]) {
			for (int j = 1; j < strlen(str); j++) {
				if (mystr[i + j] != str[j])
					break;
				return true;
			}
		}
	}
	return false;
}
bool String::IsSubstring(const String& str) {
	for (int i = 0; i < len; i++) {
		if (mystr[i] == str.mystr[0]) {
			for (int j = 1; j < strlen(str.mystr); j++) {
				if (mystr[i + j] != str.mystr[j])
					break;
				return true;
			}
		}
	}
	return false;
}
int String::str2num() {
	int m = 0;
	for (int i = 0; i < len; i++) {
		if (mystr[i] <= '9' && mystr[i] >= '0') {
			m = m * 10 + mystr[i] - '0';
		}
	}
	return m;
}
void String::toUppercase() {
	for (int i = 0; i < len; i++) {
		if (mystr[i] <= 'z' && mystr[i] >= 'a') {
			mystr[i] = mystr[i] - ('a' - 'A');
		}
	}
}
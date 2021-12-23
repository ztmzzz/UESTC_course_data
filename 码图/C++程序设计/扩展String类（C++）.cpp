#include <iostream>
using namespace std;
#include "CString.h"
#define PI 3.14

int EditString::IsSubString(int start, const char* str) {
	int i, j;
	for (i = start; i < len; i++)
	{
		int k = i;
		for (j = 0; str[j] != '\0'; j++, k++)
		{
			if (str[j] != mystr[k]) break;
		}
		if (str[j] == '\0') return i;
	}
	return -1;
}

void EditString::EditChar(char s, char d) {
	for (int i = 0; i < len; i++) {
		if (mystr[i] == s)
			mystr[i] = d;
	}
}
void EditString::EditSub(char* subs, char* subd) {
	char str[100] = { 0 };
	int t = 0;
	for (int i = 0; i < len; i++) {
		if (i == IsSubString(i, subs)) {
			for (int j = 0; j < strlen(subd); j++)
				str[t++] = subd[j];
			i += strlen(subs) - 1;
		}
		else {
			str[t++] = mystr[i];
		}
	}
	delete[]mystr;
	mystr = new char[t + 1];
	strcpy(mystr, str);
}
void EditString::DeleteChar(char ch) {
	char t[100] = { 0 };
	int k = 0;
	for (int i = 0; i < len; i++)
	{
		if (mystr[i] != ch)
		{
			t[k] = mystr[i];
			k++;
		}
	}
	delete[] mystr;
	mystr = new char[strlen(t) + 1];
	strcpy(mystr, t);
}
void EditString::DeleteSub(char* sub)
{
	char str[100] = { 0 };
	int k = 0;
	for (int i = 0; i < len; i++)
	{
		if (i == IsSubString(i, sub))
		{
			i += strlen(sub) - 1;
			continue;
		}
		str[k++] = mystr[i];
	}
	delete[]mystr;
	mystr = new char[k + 1];
	strcpy(mystr, str);
}
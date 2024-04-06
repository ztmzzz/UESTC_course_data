#include <iostream>
using namespace std;
#include "CSet.h"
bool Set::operator <=(const Set& s)const {
	//if (IsEmpty())
		//return true;
	if (n > s.n)
		return false;
	for (int i = 1; i <= n; i++) {
		if (!s.IsElement(pS[i]))
			return false;
	}
	return true;
}
bool Set::operator ==(const Set& s)const {
	if (n != s.n)
		return false;
	for (int i = 1; i <= n; i++) {
		if (!s.IsElement(pS[i]))
			return false;
	}
	return true;
}
Set& Set::operator +=(int e) {
	if (IsElement(e))
		return *this;
	int* t = new int[n + 2];
	for (int i = 1; i <= n ; i++) 
		t[i] = pS[i];
	n++;
	t[n] = e;
	delete []pS;
	pS = t;
	return *this;
}
Set& Set::operator -=(int e) {
	if (!IsElement(e))
		return *this;
	int j = 1;
	int* t = new int[n];
	for (int i = 1; i <= n; i++) {
		if (pS[i] == e)
			continue;
		t[j] = pS[i];
		j++;
	}
	n--;
	delete[]pS;
	pS = t;
	return *this;
}
Set Set::operator |(const Set& s)const {
	Set t;
	for (int i = 1; i <= n; i++) {
		t += pS[i];
	}
		
	for (int i = 1; i <= s.n; i++) {
		if (!IsElement(s.pS[i]))
			t += s.pS[i];
	}
	return t;
}
Set Set::operator &(const Set& s)const {
	Set t;
	for (int i = 1; i <= n; i++) {
		if (s.IsElement(pS[i]))
			t += pS[i];
	}
	return t;
}
Set Set::operator -(const Set& s)const {
	Set t(const_cast<Set&>(*this));
	for (int i = 1; i <= s.n; i++) {
		if (IsElement(s.pS[i]))
			t -= s.pS[i];
	}
	return t;
}
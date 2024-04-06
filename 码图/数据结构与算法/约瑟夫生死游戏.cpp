#include <iostream>
using namespace std;
//#include "Shape.h"
#define PI 3.14
typedef struct Node {
	Node* next;
	int num;
}node;

int main()
{
	int n, m, k;
	cin >> n >> m >> k;
	if (n == 1) {
		if (k == 0) {
			cout << "1 " << endl;
			return 0;
		}
		else {
			cout << endl;
			return 0;
		}
	}
	int live = n;
	node* cur = new node;
	node* head = cur;
	for (int i = 1; i < n; i++) {
		node* t = new node;
		cur->next = t;
		cur->num = i;
		cur = t;
		if (i == n-1) {
			t->next = head;
			t->num = n;
		}
	}
	cur = head;
	while (live!=k)
	{
		for (int i = 1; i < m; i++) {
			cur = cur->next;
		}
		node* before=cur;
		for (int i = 0; i < n; i++) {
			if (before->next == cur)
				break;
			before = before->next;
		}
		before->next = cur->next;
		cout << cur->num << " ";
		node* temp=cur->next;
		delete cur;
		cur = temp;
		live--;
	}
	cout << endl;
	return 0;

}
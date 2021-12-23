#include <stdio.h>
#include <malloc.h>
int index[10000000];
typedef struct Node{
	int data;
	struct Node* l, * r;
}node;
void TVisit(node* root, int* out) {
	static int n = 0;
	if (root != NULL) {
		out[n] = root->data;
		n++;
		TVisit(root->r, out);
		TVisit(root->l, out);
	}
}
node* create(int* preOrder, int* inOrder,int i,int j,int k,int h) {
	node* t = (node*)malloc(sizeof(node));
	t->data = preOrder[i];
	int m = index[preOrder[i]];
	//while (inOrder[m] != preOrder[i])
		//m++;
	if (m == k)
		t->l = NULL;
	else
		t->l = create(preOrder, inOrder, i + 1, i + m - k, k, m - 1);
	if (m == h)
		t->r = NULL;
	else
		t->r = create(preOrder, inOrder, i+m-k+1, j, m+1, h);
	return t;
}
void solve(int n, int* preOrder, int* inOrder, int* outOrder) {
	if (n <= 0)
		return;
	for (int i = 0; i < n; i++) {
		index[inOrder[i]] = i;
	}
	node* T = create(preOrder, inOrder, 0, n-1, 0, n-1);
	TVisit(T, outOrder);
}
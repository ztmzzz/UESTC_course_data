#include <stdio.h>
#include <malloc.h>
int o;
typedef struct Node {
	int data;
	struct Node* next;
}node;
typedef struct {
	int data;
	node* first;
}vnode;

void dfsa(int** a,int n,int visit[],int out[],int p) {
	static int o = 0;
	visit[p] = 1;
	out[o] = p;
	o++;
	for (int i = 0; i < n; i++) {
		if (visit[i] == 0 && a[p][i] == 1)
			dfsa(a, n, visit, out, i);
	}
}
void dfsb(vnode* a, int n, int visit[], int out[], int p) {
	static int o = 0;
	visit[p] = 1;
	out[o] = p;
	o++;
	node* t = a[p].first;
	while (t) {
		if (visit[t->data] == 0)
			dfsb(a, n, visit, out, t->data);
		t = t->next;
	}
}
void solveA(int n, int m, int e[][2], int out[]) {
	//构建矩阵
	int** a = (int**)malloc(sizeof(int*) * n);
	for (int i = 0; i < n; i++) {
		a[i] = (int*)malloc(sizeof(int) * n);
		for (int j = 0; j < n; j++) {
			a[i][j] = 0;
		}
	}
	for (int i = 0; i < m; i++) {
		int x = e[i][0]; int y = e[i][1];
		a[x][y] = 1;
		a[y][x] = 1;
	}
	//构建访问表
	int* visit = (int*)malloc(sizeof(int) * n);
	for (int i = 0; i < n; i++)
		visit[i] = 0;
	//调用
	dfsa(a, n, visit, out, 0);
	//释放内存
	for (int i = 0; i < n; i++)
		free(a[i]);
	free(a);
}

void solveB(int n, int m, int e[][2], int out[]) {
	//创建邻接表
	vnode* a = (vnode*)malloc(sizeof(vnode) * n);
	for (int i = 0; i < n; i++) {
		a[i].data = i;
		a[i].first = NULL;
	}
	for (int i = 0; i < m; i++) {
		int x = e[i][0]; int y = e[i][1];
		node* t = (node*)malloc(sizeof(node));
		t->data = y;
		t->next = NULL;
		if (a[x].first == NULL)
			a[x].first = t;
		else {
			node* p = a[x].first;
			while (p->next != NULL)
				p = p->next;
			p->next = t;
		}
		t= (node*)malloc(sizeof(node));
		t->data = x;
		t->next = NULL;
		if (a[y].first == NULL)
			a[y].first = t;
		else {
			node* p = a[y].first;
			while (p->next != NULL)
				p = p->next;
			p->next = t;
		}
	}
	//构建访问表
	int* visit = (int*)malloc(sizeof(int) * n);
	for (int i = 0; i < n; i++)
		visit[i] = 0;
	//调用
	dfsb(a, n, visit, out, 0);

}
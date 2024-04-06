#include "acllib.h"
#include <iostream>
#include <math.h>
#include <windows.h>
#include <stdlib.h>
#include <time.h>
#include "enemy.h"
#include "user.h"
#include "disp.h"
#include "keyevent.h"
#include "timeevent.h"
using namespace std;
const int winWidth = 800, winHeight = 600, fireBallWidth = 40, fireBallHeight = 38, playerWidth = 60, playerHeight = 61, lavaWidth = 140, lavaHeight = 121;
const int healthWidth = 50, healthHeight = 43, hppWidth = 40, hppHeight = 32;
double fireBallv = 2;
double healthv = 3;
int level = 0,levelup=0,over=0;
char Score[20];
double w = 0, a = 0, s = 0, d = 0;
int iskeyboard = 0;
int count = 0;
int timeinterval[3] = { 1000,4000,10000 };
time_t now, old;
ACL_Image FireBall, Player, Lava1, Lava2, Levelup, Help, P1, About, Health, Hp, Caidan;
ACL_Sound Hurt, Cure, Con;
fireball* pfireball[30] = { NULL };
lava* plava[10] = { NULL };
health* phealth = NULL;
user* User = NULL;

void KeyEvent1(int key, int event);
void KeyEvent2(int key, int event);
void KeyEvent3(int key, int event);
void TimeEvent(int timerID);
void MouseEvent(int x, int y, int button, int event);
void create(user** User);
void create(lava* lava[],int n);
void create(fireball* fireball[],int n);
void create(health** phealth);
void Delete(fireball* pfireball[], int n);
void Delete(lava* plava[], int n);
void hitAdelete();
void MouseEvent(int x, int y, int button, int event);
int hit(double x1, double y1, int w1, int h1, double x2, double y2, int w2, int h2);
void gameover();
int Setup()
{
	initWindow("小冰历险记", DEFAULT, DEFAULT, winWidth, winHeight);
	//initConsole();
	srand((unsigned)time(NULL));
	loadImage("火球.bmp", &FireBall);
	loadImage("冰.bmp", &Player);
	loadImage("池1.bmp", &Lava1);
	loadImage("池2.bmp", &Lava2);
	loadImage("升级.bmp", &Levelup);
	loadImage("帮助.bmp", &Help);
	loadImage("初始界面.bmp", &P1);
	loadImage("关于.bmp", &About);
	loadImage("蓝心.bmp", &Health);
	loadImage("心.bmp", &Hp);
	loadImage("彩蛋.bmp", &Caidan);
	loadSound("受伤.mp3", &Hurt);
	loadSound("回血.mp3", &Cure);
	loadSound("恭喜.wav", &Con);
	create(&User);
	disp1();
	registerKeyboardEvent(KeyEvent1);
	registerTimerEvent(TimeEvent);
	return 0;
}

void create(user** User) {
	*User = new user((winWidth - playerWidth) / 2, (winHeight - playerHeight) / 2, playerWidth, playerHeight,0, 10, &Player);
}
void create(lava* plava[],int n) {
	plava[n] = new lava((double)(rand() % (winWidth - lavaWidth)), (double)(rand() % (winHeight - lavaHeight)), lavaWidth, lavaHeight, time(NULL), &Lava1);
}
void create(fireball* pfireball[],int n) {
	double x, y,direction;
	if (rand() % 2)
	{
		x = rand() % 20 ;
	}
	else
	{
		x = rand() % (20) + winWidth - fireBallWidth;
	}
	if (rand() % 2)
	{
		y = rand() % 20;
	}
	else
	{
		y = -rand() % (20) + winHeight - fireBallHeight;
	}
	if (level < 3)
		direction = atan2(User->gety() - y, User->getx() - x) + rand() % (3 - level);
	else
		direction = atan2(User->gety() - y, User->getx() - x);
	pfireball[n] = new fireball(x, y, fireBallWidth, fireBallHeight, direction, fireBallv, &FireBall);
}
void create(health** phealth) {
	double x = rand() % (winWidth - healthWidth);
	double direction = (rand() % (360) - 179) / acos(-1.0);
	double y = rand() % (winHeight - healthHeight);
	*phealth = new health(x, y, healthWidth, healthHeight, direction, healthv, &Health);
}
void Delete(fireball* pfireball[], int n) {
	delete pfireball[n];
	pfireball[n] = NULL;
}
void Delete(lava* plava[], int n) {
	delete plava[n];
	plava[n] = NULL;
}
int hit(double x1, double y1, int w1, int h1, double x2, double y2, int w2, int h2)
{
	if ((x1 + w1 > x2 && x1 < x2) || (x2 + w2 > x1 && x1 > x2))
	{
		if ((y1 >= y2 && y1 < y2 + h2) || (y1 < y2 && y1 + h1 > y2))
		{
			return 1;
		}
	}
	return 0;
}
void hitAdelete()
{
	for (int i = 0; i < level + 6; i++)
	{
		if (pfireball[i] != NULL)
		{
			if (hit(pfireball[i]->getx(), pfireball[i]->gety(), fireBallWidth, fireBallHeight, User->getx(), User->gety(), playerWidth, playerHeight) == 1)
			{
				Delete(pfireball,i);
				User->lowhp();
				playSound(Hurt, 0);
			}
			else
			{
				if (pfireball[i]->getx() + fireBallWidth<0 || pfireball[i]->getx()>winWidth || pfireball[i]->gety() + fireBallHeight<0 || pfireball[i]->gety()>winHeight)
				{
					Delete(pfireball, i);
				}
			}
		}
	}
	for (int i = 0; i < level; i++)
	{
		if (plava[i] != NULL)
		{
			if (hit(plava[i]->getx(), plava[i]->gety(), lavaWidth, lavaHeight, User->getx(), User->gety(), playerWidth, playerHeight) == 1 && now - plava[i]->gettime() >= 3)
			{
				Delete(plava,i);
				User->lowhp();
				playSound(Hurt, 0);
			}
		}
	}
	if (phealth != NULL)
	{
		if (hit(phealth->getx(), phealth->gety(), healthWidth, healthHeight, User->getx(), User->gety(), playerWidth, playerHeight) == 1)
		{
			delete phealth;
			phealth = NULL;
			if (User->hp < 3)
			{
				User->addhp();
				playSound(Cure, 0);
			}
		}
		else
		{
			if (phealth->getx() + healthWidth<0 || phealth->getx()>winWidth || phealth->gety() + healthHeight<0 || phealth->gety()>winHeight)
			{
				delete phealth;
				phealth = NULL;
			}
		}

	}
	if (User->getx() + playerWidth<0 || User->getx()>winWidth || User->gety() + playerHeight<0 || User->gety()>winHeight)
	{
		::count++;
		cancelTimer(0);
		cancelTimer(1);
		cancelTimer(2);
		cancelTimer(3);
		User->move(380, 540);
		User->move(0);
		User->movegoal(User->getx() + 0.5 * playerWidth, User->gety() + 0.5 * playerHeight);
		startTimer(4, 20);
		playSound(Con, 0);
		w = a = s = d = 0;
	}
}
void MouseEvent(int x, int y, int button, int event)
{
	static int flag = 0;
	if (button == RIGHT_BUTTON && event == BUTTON_DOWN)
	{
		flag = 1;
		User->move(atan2(y - User->gety() - 0.5 * playerHeight, x - User->getx() - 0.5 * playerWidth));
		User->movegoal(x, y);
		iskeyboard = 0;
	}
	if (button == RIGHT_BUTTON && event == BUTTON_UP)
	{
		flag = 0;
		User->movegoal(x, y);
		iskeyboard = 0;
	}
	if (event == MOUSEMOVE && flag == 1)
	{
		User->move(atan2(y - User->gety() - 0.5 * playerHeight, x - User->getx() - 0.5 * playerWidth));
		User->movegoal(x, y);
	}
}
void gameover()
{
	for (int i = 0; i < 4; i++)
	{
		cancelTimer(i);
	}
	//删除物体
	for (int i = 0; i < level + 5; i++)
	{
		if (pfireball[i] != NULL)
		{
			Delete(pfireball,i);
		}
	}
	for (int i = 0; i < level; i++)
	{
		if (plava[i] != NULL)
		{
			Delete(plava,i);
		}
	}
	if (phealth != NULL)
	{
		free(phealth);
		phealth = NULL;
	}
	registerKeyboardEvent(KeyEvent3);
	sprintf(Score, "你的得分:%d", (int)User->score / 5);
	beginPaint();
	clearDevice();
	setTextSize(50);
	paintText(100, 100, Score);
	sprintf(Score, "你的等级:%d", level + 1);
	paintText(100, 200, Score);
	sprintf(Score, "找到彩蛋次数:%d", ::count);
	paintText(100, 300, Score);
	paintText(100, 400, "请按回车键重新开始");
	paintText(100, 500, "或者按ESC返回主菜单");
	endPaint();
}
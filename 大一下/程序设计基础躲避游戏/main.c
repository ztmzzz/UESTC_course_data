#include "acllib.h"
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <windows.h>

void disp1();
void disp2();
void disp3();
void disp4();
void KeyEvent1(int key, int event);
void KeyEvent2(int key, int event);
void KeyEvent3(int key, int event);
void TimeEvent(int timerID);
void MouseEvent(int x, int y, int button, int event);
void createFireBall(int n);
void deleteFireBall(int n);
void createlava(int n);
void deletelava(int n);
void createhealth();
void hitAdelete();
void gameover();
int hit(double x1, double y1, int w1, int h1, double x2, double y2, int w2, int h2);

const int winWidth = 800, winHeight = 600, fireBallWidth = 40, fireBallHeight = 38, playerWidth = 60, playerHeight = 61, lavaWidth = 140, lavaHeight = 121;
const int healthWidth = 50, healthHeight = 43, hppWidth = 40, hppHeight = 32;
int count = 0;
int level = 0;
int score = 0;
int over = 0, Levelup = 0;
int iskeyboard = 0;
int hp = 3;
int timeinterval[3] = { 1000,4000,10000 };
char Score[20];
double fireBallv = 2;
double healthv = 3;
double w = 0, a = 0, s = 0, d = 0;
time_t now, old;
ACL_Image fireBall, player, lava1, lava2, levelup, help, p1, about, health, hpp,caidan;
ACL_Sound hurt,cure,con;
struct PLAYER {
	double x, y;
	double direction;
	double velocity;
	double goalx, goaly;
}Player;
struct fireball {
	double x, y;
	double direction;
};
struct fireball* pfireBall[30] = { NULL };
struct lava {
	double x, y;
	time_t time;
};
struct lava* plava[10] = { NULL };
struct health {
	double x, y;
	double direction;
};
struct health* phealth = NULL;

int Setup()
{
	initWindow("躲避技能练习", DEFAULT, DEFAULT, winWidth, winHeight);
	//initConsole();
	srand((unsigned)time(NULL));
	loadImage("火球.bmp", &fireBall);
	loadImage("冰.bmp", &player);
	loadImage("池1.bmp", &lava1);
	loadImage("池2.bmp", &lava2);
	loadImage("升级.bmp", &levelup);
	loadImage("帮助.bmp", &help);
	loadImage("初始界面.bmp", &p1);
	loadImage("关于.bmp", &about);
	loadImage("蓝心.bmp", &health);
	loadImage("心.bmp", &hpp);
	loadImage("彩蛋.bmp", &caidan);
	loadSound("受伤.mp3", &hurt);
	loadSound("回血.mp3", &cure);
	loadSound("恭喜.wav", &con);
	Player.x = (winWidth - playerWidth) / 2;
	Player.y = (winHeight - playerHeight) / 2;
	Player.direction = 0;
	Player.velocity = 10;
	Player.goalx = Player.x + 0.5 * playerWidth;
	Player.goaly = Player.y + 0.5 * playerHeight;
	disp1();
	registerKeyboardEvent(KeyEvent1);
	registerTimerEvent(TimeEvent);
	return 0;
}
void disp1()
{
	beginPaint();
	clearDevice();
	putImage(&p1, 0, 0);
	endPaint();
}
void disp2()
{
	beginPaint();
	clearDevice();
	putImage(&help, 0, 0);
	endPaint();
}
void disp3()
{
	beginPaint();
	clearDevice();
	setTextSize(40);
	paintText(300, 20, Score);
	paintText(20, 20, "血量:");
	for (int i = 0; i < hp; i++)
	{
		putImageTransparent(&hpp, 120 + i * hppWidth, 25, hppWidth, hppHeight, WHITE);
	}
	for (int i = 0; i < level + 5; i++)
	{
		if (pfireBall[i] != NULL)
		{
			putImageTransparent(&fireBall, pfireBall[i]->x, pfireBall[i]->y, fireBallWidth, fireBallHeight, WHITE);
		}
	}
	for (int i = 0; i < level; i++)
	{
		if (plava[i] != NULL)
		{
			if (now - plava[i]->time >= 3)
			{
				putImageTransparent(&lava2, plava[i]->x, plava[i]->y, lavaWidth, lavaHeight, WHITE);
			}
			else
			{
				putImageTransparent(&lava1, plava[i]->x, plava[i]->y, lavaWidth, lavaHeight, WHITE);
			}
		}
	}
	if (phealth != NULL)
	{
		putImageTransparent(&health, phealth->x, phealth->y, healthWidth, healthHeight, WHITE);
	}
	putImageTransparent(&player, Player.x, Player.y, playerWidth, playerHeight, WHITE);
	if (Levelup == 1)
	{
		putImageTransparent(&levelup, Player.x, Player.y - 40, 50, 35, WHITE);
	}
	endPaint();
}
void disp4()
{
	beginPaint();
	clearDevice();
	putImage(&about, 0, 0);
	endPaint();
}
void KeyEvent1(int key, int event)
{
	if (key == 0x48 && event == KEY_DOWN)//H
	{
		disp2();
	}
	if (key == 0x41 && event == KEY_DOWN)//A
	{
		disp4();
	}
	if (key == VK_RETURN && event == KEY_DOWN)
	{
		disp3();
		registerKeyboardEvent(KeyEvent2);
		registerMouseEvent(MouseEvent);
		startTimer(1, timeinterval[0]);
		startTimer(3, timeinterval[2]);
		startTimer(0, 20);
	}
	if (key == VK_ESCAPE && event == KEY_DOWN)
	{
		disp1();
	}
}
void KeyEvent2(int key, int event)
{
	if (key == 0x57 && event == KEY_DOWN)//W
	{
		if (s == 1)
			s = 0;
		w = -1;
		iskeyboard = 1;
	}
	if (key == 0x57 && event == KEY_UP)//W
	{
		w = 0;
		iskeyboard = 1;
	}
	if (key == 0x53 && event == KEY_DOWN)//S
	{
		if (w == -1)
			w = 0;
		s = 1;
	}
	if (key == 0x53 && event == KEY_UP)//S
	{
		s = 0;
		iskeyboard = 1;
	}
	if (key == 0x41 && event == KEY_DOWN)//A
	{
		if (d == 1)
			d = 0;
		a = -1;
		iskeyboard = 1;
	}
	if (key == 0x41 && event == KEY_UP)//A
	{
		a = 0;
		iskeyboard = 1;
	}
	if (key == 0x44 && event == KEY_DOWN)//D
	{
		if (a == -1)
			a = 0;
		d = 1;
		iskeyboard = 1;
	}
	if (key == 0x44 && event == KEY_UP)//D
	{
		d = 0;
		iskeyboard = 1;
	}
	if (abs(w + s + a + d) == 2 || w + s + a + d == 0)
	{
		w /= sqrt(2);
		s /= sqrt(2);
		a /= sqrt(2);
		d /= sqrt(2);
	}

}
void KeyEvent3(int key, int event)
{
	if (key == VK_RETURN && event == KEY_DOWN)
	{
		count = 0;
		hp = 3;
		healthv = 3;
		timeinterval[0] = 1000;
		timeinterval[1] = 6000;
		timeinterval[2] = 10000;
		fireBallv = 2;
		level = 0;
		w = 0; a = 0; s = 0; d = 0;
		score = 0;
		over = 0;
		Levelup = 0;
		iskeyboard = 0;
		Player.x = (winWidth - playerWidth) / 2;
		Player.y = (winHeight - playerHeight) / 2;
		Player.direction = 0;
		Player.velocity = 10;
		Player.goalx = Player.x + 0.5 * playerWidth;
		Player.goaly = Player.y + 0.5 * playerHeight;
		disp3();
		registerKeyboardEvent(KeyEvent2);
		registerMouseEvent(MouseEvent);
		startTimer(1, timeinterval[0]);
		startTimer(3, timeinterval[2]);
		startTimer(0, 20);
	}
	if (key == VK_ESCAPE && event == KEY_DOWN)
	{
		count = 0;
		hp = 3;
		healthv = 3;
		timeinterval[0] = 1000;
		timeinterval[1] = 6000;
		timeinterval[2] = 10000;
		fireBallv = 2;
		level = 0;
		w = 0; a = 0; s = 0; d = 0;
		score = 0;
		over = 0;
		Levelup = 0;
		iskeyboard = 0;
		Player.x = (winWidth - playerWidth) / 2;
		Player.y = (winHeight - playerHeight) / 2;
		Player.direction = 0;
		Player.velocity = 10;
		Player.goalx = Player.x + 0.5 * playerWidth;
		Player.goaly = Player.y + 0.5 * playerHeight;
		disp1();
		registerKeyboardEvent(KeyEvent1);
	}
}
void MouseEvent(int x, int y, int button, int event)
{
	static int flag = 0;
	if (button == RIGHT_BUTTON && event == BUTTON_DOWN)
	{
		flag = 1;
		Player.direction = atan2(y - Player.y - 0.5 * playerHeight, x - Player.x - 0.5 * playerWidth);
		Player.goalx = x;
		Player.goaly = y;
		iskeyboard = 0;
	}
	if (button == RIGHT_BUTTON && event == BUTTON_UP)
	{
		flag = 0;
		Player.goalx = x;
		Player.goaly = y;
		iskeyboard = 0;
	}
	if (event == MOUSEMOVE && flag == 1)
	{
		Player.direction = atan2(y - Player.y - 0.5 * playerHeight, x - Player.x - 0.5 * playerWidth);
		Player.goalx = x;
		Player.goaly = y;
	}
}
void TimeEvent(int timerID)
{
	if (timerID == 0)
	{
		now = time(NULL);
		//障碍物移动
		for (int i = 0; i < level + 6; i++)
		{
			if (pfireBall[i] != NULL)
			{
				pfireBall[i]->x += cos(pfireBall[i]->direction) * fireBallv;
				pfireBall[i]->y += sin(pfireBall[i]->direction) * fireBallv;
			}
		}
		for (int i = 0; i < level; i++)
		{
			if (plava[i] != NULL && now - plava[i]->time >= 3)
			{

				if (now - plava[i]->time >= 5)
				{
					deletelava(i);
				}
			}
		}
		//冰块移动
		if (iskeyboard == 1)
		{
			Player.x += (a + d) * Player.velocity;
			Player.y += (w + s) * Player.velocity;
		}
		else
		{
			if (abs(-Player.goalx + Player.x + 0.5 * playerWidth) > 5)
			{
				Player.x += cos(Player.direction) * Player.velocity;
			}
			if (abs(-Player.goaly + Player.y + 0.5 * playerHeight) > 5)
			{
				Player.y += sin(Player.direction) * Player.velocity;
			}
		}
		//蓝心移动
		if (phealth != NULL)
		{
			phealth->x += cos(phealth->direction) * healthv;
			phealth->y += sin(phealth->direction) * healthv;
		}
		hitAdelete();
		score++;
		//升级
		if (score == 300)//level2
		{
			level++;
			startTimer(2, timeinterval[1]);
			Levelup = 1;
			old = time(NULL);
			fireBallv++;
		}
		if (score == 600)//level3
		{
			level++;
			Levelup = 1;
			old = time(NULL);
			Player.velocity--;
			fireBallv++;
			healthv++;
		}
		if (score == 1200)//level4
		{
			level++;
			Levelup = 1;
			old = time(NULL);
			fireBallv++;
		}
		if (score == 1800)//level5
		{
			level++;
			Levelup = 1;
			old = time(NULL);
			Player.velocity--;
			fireBallv++;
			healthv++;
		}
		if (score == 2400)//level6
		{
			level++;
			Levelup = 1;
			old = time(NULL);
			Player.velocity--;
			fireBallv++;
			healthv++;
		}
		//升级显示
		if (Levelup == 1 && now - old >= 3)
		{
			Levelup = 0;
		}
		sprintf(Score, "分数:%d", score / 5);
		disp3();
		if (hp <= 0)
		{
			gameover();
		}

	}
	if (timerID == 1)
	{
		for (int i = 0; i < level + 6; i++)
		{
			if (pfireBall[i] == NULL)
			{
				createFireBall(i);
				break;
			}
		}
	}
	if (timerID == 2)
	{
		for (int i = 0; i < level; i++)
		{
			if (plava[i] == NULL)
			{
				createlava(i);
				break;
			}
		}
	}
	if (timerID == 3)
	{
		if (phealth == NULL)
		{
			createhealth();
		}
	}
	if (timerID == 4)
	{
		if (iskeyboard == 1)
		{
			Player.x += (a + d) * Player.velocity;
			Player.y += (w + s) * Player.velocity;
		}
		else
		{
			if (abs(-Player.goalx + Player.x + 0.5 * playerWidth) > 5)
			{
				Player.x += cos(Player.direction) * Player.velocity;
			}
			if (abs(-Player.goaly + Player.y + 0.5 * playerHeight) > 5)
			{
				Player.y += sin(Player.direction) * Player.velocity;
			}
		}
		beginPaint();
		putImage(&caidan, 0, 0);
		putImageTransparent(&player, Player.x, Player.y, playerWidth, playerHeight, WHITE);
		endPaint();
		if (Player.x + playerWidth<0 || Player.x>winWidth || Player.y + playerHeight<0 || Player.y>winHeight)
		{
			cancelTimer(4);
			startTimer(0,20);
			startTimer(1, timeinterval[0]);
			startTimer(3, timeinterval[2]);
			if (level >= 1)
			{
				startTimer(2, timeinterval[1]);
			}
			Player.x = (winWidth - playerWidth) / 2;
			Player.y = (winHeight - playerHeight) / 2;
			Player.direction = 0;
			Player.goalx = Player.x + 0.5 * playerWidth;
			Player.goaly = Player.y + 0.5 * playerHeight;
		}
	}
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
		if (pfireBall[i] != NULL)
		{
			if (hit(pfireBall[i]->x, pfireBall[i]->y, fireBallWidth, fireBallHeight, Player.x, Player.y, playerWidth, playerHeight) == 1)
			{
				deleteFireBall(i);
				hp--;
				playSound(hurt, 0);
			}
			else
			{
				if (pfireBall[i]->x + fireBallWidth<0 || pfireBall[i]->x>winWidth || pfireBall[i]->y + fireBallHeight<0 || pfireBall[i]->y>winHeight)
				{
					deleteFireBall(i);
				}
			}
		}
	}
	for (int i = 0; i < level; i++)
	{
		if (plava[i] != NULL)
		{
			if (hit(plava[i]->x, plava[i]->y, lavaWidth, lavaHeight, Player.x, Player.y, playerWidth, playerHeight) == 1 && now-plava[i]->time>=3)
			{
				deletelava(i);
				hp--;
				playSound(hurt, 0);
			}
		}
	}
	if (phealth != NULL)
	{
		if (hit(phealth->x, phealth->y, healthWidth, healthHeight, Player.x, Player.y, playerWidth, playerHeight) == 1)
		{
			free(phealth);
			phealth = NULL;
			if (hp < 3)
			{
				hp++;
				playSound(cure, 0);
			}
		}
		else
		{
			if (phealth->x + healthWidth<0 || phealth->x>winWidth || phealth->y + healthHeight<0 || phealth->y>winHeight)
			{
				free(phealth);
				phealth = NULL;
			}
		}

	}
	if (Player.x + playerWidth<0 || Player.x>winWidth || Player.y + playerHeight<0 || Player.y>winHeight)
	{
		count++;
		cancelTimer(0);
		cancelTimer(1);
		cancelTimer(2);
		cancelTimer(3);
		startTimer(4, 20);
		playSound(con, 0);
		w = a = s = d = 0;
		Player.x = 380;
		Player.y = 540;
		Player.direction = 0;
		Player.goalx = Player.x + 0.5 * playerWidth;
		Player.goaly = Player.y + 0.5 * playerHeight;
	}
}
void createFireBall(int n)
{
	pfireBall[n] = (struct fireball*)malloc(sizeof(struct fireball));
	if (rand() % 2)
	{
		pfireBall[n]->x = rand() % 20;
	}
	else
	{
		pfireBall[n]->x = rand() % (20) + winWidth - fireBallWidth;
	}
	if (rand() % 2)
	{
		pfireBall[n]->y = rand() % 20;
	}
	else
	{
		pfireBall[n]->y = -rand() % (20) + winHeight - fireBallHeight;
	}
	/*pfireBall[n]->x = rand() % ( winWidth - fireBallWidth);
	pfireBall[n]->y = rand() % (winHeight - fireBallHeight);*/
	if(level<3)
		pfireBall[n]->direction = atan2(Player.y - pfireBall[n]->y, Player.x - pfireBall[n]->x) + rand() % (3 - level);
	else
		pfireBall[n]->direction = atan2(Player.y - pfireBall[n]->y, Player.x - pfireBall[n]->x);
}
void deleteFireBall(int n)
{
	free(pfireBall[n]);
	pfireBall[n] = NULL;
}
void createlava(int n)
{
	plava[n] = (struct lava*)malloc(sizeof(struct lava));
	/*if (rand() % 2 && (int)Player.x - lavaWidth>0)
	{
		plava[n]->x = rand() % ((int)Player.x-lavaWidth);
	}
	else
	{
		pfireBall[n]->x = rand() % (winWidth-lavaWidth- (int)Player.x-playerWidth)+ (int)Player.x + playerWidth;
	}
	if (rand() % 2 && (int)Player.y - lavaHeight > 0)
	{
		plava[n]->y = rand() % ((int)Player.y - lavaHeight);
	}
	else
	{
		pfireBall[n]->y = rand() % (winHeight - lavaHeight - (int)Player.y - playerHeight) + (int)Player.y + playerHeight;
	}岩浆池无需避开冰*/
	plava[n]->x = rand() % (winWidth - lavaWidth);
	plava[n]->y = rand() % (winHeight - lavaHeight);
	plava[n]->time = time(NULL);
}
void deletelava(int n)
{
	free(plava[n]);
	plava[n] = NULL;
}
void createhealth()
{
	phealth = (struct health*)malloc(sizeof(struct health));
	phealth->x = rand() % (winWidth - healthWidth);
	phealth->y = rand() % (winHeight - healthHeight);
	phealth->direction = (rand() % (360) - 179) / acos(-1.0);
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
		if (pfireBall[i] != NULL)
		{
			deleteFireBall(i);
		}
	}
	for (int i = 0; i < level; i++)
	{
		if (plava[i] != NULL)
		{
			deletelava(i);
		}
	}
	if (phealth != NULL)
	{
		free(phealth);
		phealth = NULL;
	}
	registerKeyboardEvent(KeyEvent3);
	sprintf(Score, "你的得分:%d", (int)score / 5);
	beginPaint();
	clearDevice();
	setTextSize(50);
	paintText(100, 100, Score);
	sprintf(Score, "你的等级:%d", level + 1);
	paintText(100, 200, Score);
	sprintf(Score, "找到彩蛋次数:%d", count);
	paintText(100, 300, Score);
	paintText(100, 400, "请按回车键重新开始");
	paintText(100, 500, "或者按ESC返回主菜单");
	endPaint();
}
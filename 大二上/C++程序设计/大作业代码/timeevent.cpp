#include "timeevent.h"
void addspeed(fireball* pfireball[]) {
	for (int i = 0; i < level + 6; i++) {
		if (pfireball[i] != NULL)
		{
			pfireball[i]->addspeed();
		}
	}
}
void addspeed(health* phealth) {
	if (phealth != NULL)
	{
		phealth->addspeed();
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
			if (pfireball[i] != NULL)
			{
				pfireball[i]->change();
			}
		}
		for (int i = 0; i < level; i++)
		{
			if (plava[i] != NULL && now - plava[i]->gettime() >= 5)
				Delete(plava,i);
		}
		//冰块移动
		User->change(iskeyboard);
		//蓝心移动
		if (phealth != NULL)
		{
			phealth->change();
		}
		hitAdelete();
		User->addscore();
		//升级
		if (User->getscore() == 300)//level2
		{
			level++;
			startTimer(2, timeinterval[1]);
			levelup = 1;
			old = time(NULL);
			addspeed(pfireball);
		}
		if (User->getscore() == 600)//level3
		{
			level++;
			levelup = 1;
			old = time(NULL);
			User->lowspeed();
			addspeed(pfireball);
			addspeed(phealth);
		}
		if (User->getscore() == 1200)//level4
		{
			level++;
			levelup = 1;
			old = time(NULL);
			addspeed(pfireball);
		}
		if (User->getscore() == 1800)//level5
		{
			level++;
			levelup = 1;
			old = time(NULL);
			User->lowspeed();
			addspeed(pfireball);
			addspeed(phealth);
		}
		if (User->getscore() == 2400)//level6
		{
			level++;
			levelup = 1;
			old = time(NULL);
			User->lowspeed();
			addspeed(pfireball);
			addspeed(phealth);
		}
		//升级显示
		if (levelup == 1 && now - old >= 3)
		{
			levelup = 0;
		}
		sprintf(Score, "分数:%d", User->score / 5);
		disp3();
		if (User->hp <= 0)
		{
			gameover();
		}

	}
	if (timerID == 1)
	{
		for (int i = 0; i < level + 6; i++)
		{
			if (pfireball[i] == NULL)
			{
				create(pfireball,i);
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
				create(plava,i);
				break;
			}
		}
	}
	if (timerID == 3)
	{
		if (phealth == NULL)
		{
			create(&phealth);
		}
	}
	if (timerID == 4)
	{
		User->change(iskeyboard);
		beginPaint();
		putImage(&Caidan, 0, 0);
		putImageTransparent(&Player, User->getx(), User->gety(), playerWidth, playerHeight, WHITE);
		endPaint();
		if (User->getx() + playerWidth<0 || User->getx()>winWidth || User->gety() + playerHeight<0 || User->gety()>winHeight)
		{
			cancelTimer(4);
			startTimer(0, 20);
			startTimer(1, timeinterval[0]);
			startTimer(3, timeinterval[2]);
			if (level >= 1)
			{
				startTimer(2, timeinterval[1]);
			}
			User->move((winWidth - playerWidth) / 2, (winHeight - playerHeight) / 2);
			User->move(0);
			User->movegoal(User->getx() + 0.5 * playerWidth, User->gety() + 0.5 * playerHeight);
		}
	}
}
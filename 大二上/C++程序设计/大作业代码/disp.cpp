#include "disp.h"

void disp1()
{
	beginPaint();
	clearDevice();
	putImage(&P1, 0, 0);
	endPaint();
}
void disp2()
{
	beginPaint();
	clearDevice();
	putImage(&Help, 0, 0);
	endPaint();
}
void disp3()
{
	beginPaint();
	clearDevice();
	setTextSize(40);
	paintText(300, 20, Score);
	paintText(20, 20, "ÑªÁ¿:");
	for (int i = 0; i < User->hp; i++)
	{
		putImageTransparent(&Hp, 120 + i * hppWidth, 25, hppWidth, hppHeight, WHITE);
	}
	for (int i = 0; i < level + 5; i++)
	{
		if (pfireball[i] != NULL)
		{
			putImageTransparent(&FireBall, pfireball[i]->getx(), pfireball[i]->gety(), fireBallWidth, fireBallHeight, WHITE);
		}
	}
	for (int i = 0; i < level; i++)
	{
		if (plava[i] != NULL)
		{
			if (now - plava[i]->gettime() >= 3)
			{
				putImageTransparent(&Lava2, plava[i]->getx(), plava[i]->gety(), lavaWidth, lavaHeight, WHITE);
			}
			else
			{
				putImageTransparent(&Lava1, plava[i]->getx(), plava[i]->gety(), lavaWidth, lavaHeight, WHITE);
			}
		}
	}
	if (phealth != NULL)
	{
		putImageTransparent(&Health, phealth->getx(), phealth->gety(), healthWidth, healthHeight, WHITE);
	}
	putImageTransparent(&Player, User->getx(), User->gety(), playerWidth, playerHeight, WHITE);
	if (levelup == 1)
	{
		putImageTransparent(&Levelup, User->getx(), User->gety() - 40, 50, 35, WHITE);
	}
	endPaint();
}
void disp4()
{
	beginPaint();
	clearDevice();
	putImage(&About, 0, 0);
	endPaint();
}
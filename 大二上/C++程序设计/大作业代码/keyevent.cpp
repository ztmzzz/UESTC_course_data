#include "keyevent.h"
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
	if (abs((int)(w + s + a + d)) == 2 || w + s + a + d == 0)
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
		healthv = 3;
		timeinterval[0] = 1000;
		timeinterval[1] = 6000;
		timeinterval[2] = 10000;
		fireBallv = 2;
		level = 0;
		w = 0; a = 0; s = 0; d = 0;
		over = 0;
		levelup = 0;
		iskeyboard = 0;
		User->reset();
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
		healthv = 3;
		timeinterval[0] = 1000;
		timeinterval[1] = 6000;
		timeinterval[2] = 10000;
		fireBallv = 2;
		level = 0;
		w = 0; a = 0; s = 0; d = 0;
		over = 0;
		levelup = 0;
		iskeyboard = 0;
		User->reset();
		disp1();
		registerKeyboardEvent(KeyEvent1);
	}
}
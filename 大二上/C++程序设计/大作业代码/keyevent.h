#pragma once
#include "acllib.h"
#include "disp.h"
#include <math.h>
extern int iskeyboard,count,over;
extern double w, a, s, d, healthv, fireBallv;
extern int timeinterval[3];
extern user* User;
extern void MouseEvent(int x, int y, int button, int event);
void KeyEvent1(int key, int event);
void KeyEvent2(int key, int event);
void KeyEvent3(int key, int event);
#pragma once
#include "keyevent.h"
#include <stdlib.h>
#include <iostream>
#include "disp.h"
#include "enemy.h"
#include "user.h"
extern int timeinterval[3];
extern time_t old;
void TimeEvent(int timerID);
extern void create(user** User);
extern void create(lava* lava[], int n);
extern void create(fireball* fireball[], int n);
extern void create(health** phealth);
extern void Delete(fireball* pfireball[], int n);
extern void Delete(lava* plava[], int n);
extern void hitAdelete();
extern void gameover();
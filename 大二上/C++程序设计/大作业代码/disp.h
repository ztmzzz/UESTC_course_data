#pragma once
#include "acllib.h"
#include "user.h"
extern const int hppWidth, hppHeight, fireBallWidth, fireBallHeight, lavaWidth,lavaHeight, healthWidth, healthHeight, playerWidth, playerHeight;
extern ACL_Image FireBall, Player, Lava1, Lava2, Levelup, Help, P1, About, Health, Hp, Caidan;
extern char Score[];
extern user* User;
extern int level,levelup;
extern lava* plava[];
extern fireball* pfireball[];
extern health* phealth;
extern time_t now;
void disp1();
void disp2();
void disp3();
void disp4();
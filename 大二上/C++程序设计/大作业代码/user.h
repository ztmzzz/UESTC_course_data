#pragma once
#include "acllib.h"
#include "enemy.h"
#include <math.h>
extern const int winWidth, winHeight,playerWidth, playerHeight;
extern double w, a, d, s;
class user :public base {
protected:
	double speed;
	double direction;
	double goalx, goaly;
public:
	int score;
	int hp;
	user(double x, double y, int w, int h, double d, double speed,ACL_Image* pImage);
	virtual ~user();
	void change(int i);
	void move(double x, double y);
	void move(double d);
	void movegoal(double x,double y);
	void reset();
	void addscore();
	int getscore();
	void lowspeed();
	void addhp();
	void lowhp();
	//friend void TimeEvent(int timerID);
	//friend void MouseEvent(int x, int y, int button, int event);
};
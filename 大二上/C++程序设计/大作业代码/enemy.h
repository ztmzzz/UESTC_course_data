#pragma once
#include "acllib.h"
#include <time.h>
class base {
protected:
	double x, y;
	int w, h;
	ACL_Image* pImage;
public:
	base(double x, double y, int w, int h, ACL_Image* pImage);
	virtual ~base();
	void drawBase();
	virtual void move(double x,double y);
	double getx();
	double gety();
	virtual void change();
	
};
class fireball :public base {
protected:
	double speed;
	double direction;
public:
	fireball(double x, double y, int w, int h, double d, double speed, ACL_Image* pImage);
	virtual ~fireball();
	double getdir();
	//friend void TimeEvent(int timerID);
	void change();
	virtual void addspeed();

};
class health :public fireball {
public:
	health(double x, double y, int w, int h, double d, double speed, ACL_Image* pImage);
	virtual ~health();
	void change();
	
};
class lava :public base {
protected:
	time_t time;
public:
	lava(double x, double y, int w, int h, time_t time, ACL_Image* pImage);
	virtual ~lava();
	time_t gettime();
	//friend void TimeEvent(int timerID);
};

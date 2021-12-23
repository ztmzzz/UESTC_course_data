#include "user.h"

user::user(double x, double y, int w, int h, double d, double speed, ACL_Image* pImage):base(x, y, w, h, pImage) {
	this->score = 0;
	this->direction = d;
	this->speed = speed;
	this->hp = 3;
	this->goalx = x + 0.5 * playerWidth;
	this->goaly = y + 0.5 * playerHeight;
}
user::~user() {

}
void user::change(int i) {
	if (i == 1) {
		this->x += (a + d) * this->speed;
		this->y += (::w + s) * this->speed;
	}
	else {
		if (fabs(-this->goalx + this->x + 0.5 * playerWidth) > 5)
		{
			this->x += cos(this->direction) * this->speed;
		}
		if (fabs(-this->goaly + this->y + 0.5 * playerWidth) > 5)
		{
			this->y += sin(this->direction) * this->speed;
		}
	}
}

void user::move(double x, double y)
{
	this->x = x;
	this->y = y;
}

void user::reset() {
	this->x = (winWidth - playerWidth) / 2;
	this->y = (winHeight - playerHeight) / 2;
	this->direction = 0;
	this->speed = 10;
	this->score = 0;
	this->hp = 3;
	this->goalx = x + 0.5 * playerWidth;
	this->goaly = y + 0.5 * playerHeight;

}

void user::addscore()
{
	this->score++;
}

int user::getscore()
{
	return score;
}

void user::lowspeed()
{
	speed--;
}

void user::addhp()
{
	hp++;
}

void user::lowhp()
{
	hp--;
}

void user::move(double d) {
	this->direction = d;
}
void user::movegoal(double x,double y){
	this->goalx = x;
	this->goaly = y;
}

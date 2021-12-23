#include "enemy.h"
#include <math.h>
extern ACL_Image Lava2;
base::base(double x, double y, int w, int h, ACL_Image* pImage) {
	this->x = x;
	this->y = y;
	this->w = w;
	this->h = h;
	this->pImage = pImage;
}
base::~base() {

}
void base::drawBase() {
	putImageTransparent(pImage, x, y, w, h, WHITE);
}

double base::getx() {
	return x;
}
double base::gety() {
	return y;
}
void base::change()
{
}
void base::move(double x, double y) {
	this->x = x;
	this->y = y;
}
fireball::fireball(double x, double y, int w, int h, double d, double speed, ACL_Image* pImage) :base( x,  y,  w,  h, pImage) {
	this->direction = d;
	this->speed = speed;
}
fireball::~fireball() {

}
void fireball::change() {
	this->x += cos(this->direction) * this->speed;
	this->y += sin(this->direction) * this->speed;
}

void fireball::addspeed()
{
	speed++;
}

double fireball::getdir() {
	return direction;
}


health::health(double x, double y, int w, int h, double d, double speed, ACL_Image* pImage) :fireball(x, y, w, h, d, speed, pImage) {

}
health::~health() {

}

void health::change()
{
	this->x += cos(this->direction) * speed;
	this->y += sin(this->direction) * speed;
}


lava::lava(double x, double y, int w, int h, time_t time, ACL_Image* pImage) : base(x, y, w, h, pImage) {
	this->time = time;
}
lava::~lava() {

}


time_t lava::gettime() {
	return time;
}
#include <iostream> 
#include "CPoint.h"
#define PI 3.14
using namespace std;

Rectangle::Rectangle(float xx, float yy, float w, float h):Point(xx, yy) {
    width = w; high = h; 
}
float Rectangle::Area() {
    return width * high;
}
Circle::Circle(float xx, float yy, float r) :Point(xx, yy) {
    radius = r;
}
float Circle::Area() {
    return PI * radius * radius;
}
#include <stdio.h>
#include <stdlib.h>

int main()
{
    const float pi = 3.14;
    float a, b;
    scanf("%f %f", &a,&b);

    printf("area=%.2f,volume=%.2f", pi*a*a, pi * a * a*b);
    

}
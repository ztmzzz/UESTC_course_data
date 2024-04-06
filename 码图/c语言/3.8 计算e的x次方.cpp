#include <stdio.h>
#include <stdlib.h>
#include <math.h>

unsigned long long int jc(int n)
{
    if (n >= 1)
        return n * jc(n - 1);
    else
        return 1;
}
int main()
{
    double x, n, ans=0;
    scanf("%lf %lf", &x, &n);
    if (n < 0 )
    {
        printf("error");
        return 0;
    }
    if (x == 0)
    {
        printf("1.000000");
        return 0;
    }
    ans = 1 + x;
    for (int i = 2; i <= n; i++)
    {
        ans += pow(x,i) / jc(i);
    }
    printf("%.6f",ans);
}
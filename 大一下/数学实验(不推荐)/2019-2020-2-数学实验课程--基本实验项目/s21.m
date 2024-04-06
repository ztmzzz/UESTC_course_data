function r=myfun
clear;
syms x a;
y=a*exp(x)/sqrt(a^2+x^2);
z=diff(y,x,2);
r=subs(z,x,5*a);



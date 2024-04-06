function r=myfun2
syms x;
y=1/(1+x^2);
r=taylor(y,x,'Order',6);

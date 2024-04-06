for i=1:7
   eval(strcat('syms x',num2str(i)));
end
funy = 174.42*(x1/x5)*(x3/(x2 - x1))^0.85*...
    sqrt((1 - 2.62*(1 - 0.36*(x4/x2)^(-0.56))^(3/2)*(x4/x2)^1.16)/(x6*x7));
for i=1:7
   eval(sprintf("f%d=diff(funy,x%d);",i,i));
end
for i=1:7
   eval(sprintf("g%d=matlabFunction(f%d);",i,i));
end
T=taylor(funy,[x1 x2 x3 x4 x5 x6 x7],[0.1 0.3 0.1 0.1 1.5 16 0.75],'order',2)
y=matlabFunction(T);
y(0.1,0.3,0.1,0.1,1.5,16,0.75)
y(0.11,0.36,0.08,0.09,1.6,14,0.65)
y(0.09,0.25,0.08,0.11,1.7,18,0.9)
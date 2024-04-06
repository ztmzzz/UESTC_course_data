y=zeros(1,100000);
for i=1:100000
x=-2+4*rand;
y(i)=5*x^2-exp(x*sin(x))-8;
end
min(y)

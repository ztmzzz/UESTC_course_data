N=10000000;
x3=0:25;
x1=unifrnd(0,15,1,N);
x2=unifrnd(0,9,1,N);
f=@(x1,x2,x3)(2*(x1-1)^2+3*(x2-4)^2+x1*x2+(2*x3-5)^2);
mx1=0;mx2=0;mx3=0;fmin=f(0,0,0);
for x3=0:25
    for i=1:N
        if(3*x1(i)+2*x2(i)+6*x3<=20&&4*x1(i)+5*x2(i)+2*x3<=21)
            tmin=f(x1(i),x2(i),x3);
            if(tmin<fmin)
                fmin=tmin;
                mx1=x1(i);mx2=x2(i);mx3=x3;
            end
        end
    end
end
mx1
mx2
mx3
fmin
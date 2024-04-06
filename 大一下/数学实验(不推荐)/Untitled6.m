clear
syms x y u v;
N=1000;%到1W将占用大量内存
xmin=1;xmax=2;ymin=1;ymax=2;
x1=linspace(xmin,xmax,N);
y1=linspace(ymin,ymax,N);
[X,Y]=meshgrid(x1,y1);
zxy=x^y+x^2;
solve(x==v+u,y==v-u,u,v);
x=v+u;
y=v-u;
J=abs(det([diff(x,u) diff(x,v);diff(y,u) diff(y,v)]));
uxy=ans.u(1,1);
vxy=ans.v(1,1);
zuv=(x^y+x^2)*J;
uxy1=matlabFunction(uxy);
U=uxy1(X,Y);
vxy1=matlabFunction(vxy);
V=vxy1(X,Y);
f1=matlabFunction(zxy);
f2=matlabFunction(zuv);
result1=integral2(f1,xmin,xmax,ymin,ymax);
result2=0;
for i=1:N-1
    for j=1:N-1
       % result2=result2+f2(U(i,j),V(i,j))*abs(sqrt(((U(i,j)-U(i,j+1))^2+(V(i,j)-V(i,j+1))^2))*sqrt(((U(i,j)-U(i+1,j))^2+(V(i,j)-V(i+1,j))^2)));
        s1 = helen([U(i,j),V(i,j)],[U(i+1,j),V(i+1,j)],[U(i,j+1),V(i,j+1)]);
        s2 = helen([U(i,j),V(i,j)],[U(i+1,j+1),V(i+1,j+1)],[U(i,j+1),V(i,j+1)]);
        s = s1+s2;
        result2=result2+f2(U(i,j),V(i,j))*s;
    end
end
figure()
subplot(1,2,1);
plot3(X,Y,f1(X,Y),'o');
title('xy坐标下');
subplot(1,2,2);
plot3(U,V,f2(U,V),'o');
title('uv坐标下');
fprintf("xy下积分结果为%f\nuv下积分结果为%f\n",result1,result2);

 function s = helen(x,y,z)
a = lenth(x,y);
b = lenth(x,z);
c = lenth(y,z);
p = (a+b+c)/2;
s = sqrt(p*(p-a)*(p-b)*(p-c));
 end
function len = lenth(x,y)
len = sqrt((x(1)-y(1))^2+(x(2)-y(2))^2);
end
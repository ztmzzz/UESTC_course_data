clear
syms x y u v f a b c d f2;
xmin=0;xmax=2;ymin=0;ymax=2;
a=1;b=1;c=1;d=1;
f=x+y;
jf=integral2(matlabFunction(f),xmin,xmax,ymin,ymax)
A=[a b;c d];
B=[x;y];    
X=[u;v];
x=a*u+b*v;
y=c*u+d*v;
j=[diff(x,u) diff(x,v);diff(y,u) diff(y,v)];
J=abs(det(j));
X=A\B;
u=X(1,1);
u1=matlabFunction(u);
v=X(2,1);
v1=matlabFunction(v);
f2=x*y;
if(d>=0 && b>=0)
    umin=u1(xmin,ymax);
    umax=u1(xmax,ymin);
elseif (d>=0)
    umin=u1(xmin,ymin);
    umax=u1(xmax,ymax);
elseif (b>=0)
    umin=u1(xmax,ymax);
    umax=u1(xmin,ymin);
else
    umin=u1(xmax,ymin);
    umax=u1(xmin,ymax);
end
if (a*d-b*c <0)
    t=umax;umax=umin;umin=t;
end
f3=matlabFunction(f2*J);
jq=0;
%vmin=linprog([d/b],[d/b;-d/b],[u/b+ymax;-u/b-ymin],[],[],[xmin],[xmax])-u/b
%vmax=linprog([-d/b],[d/b;-d/b],[u/b+ymax;-u/b-ymin],[],[],[xmin],[xmax])-u/b
%jq=integral2(matlabFunction(f2),umin,umax,linprog([d/b],[d/b;-d/b],[x/b+ymax;-u/b-ymin],[],[],[xmin],[xmax])-u/b,linprog([-d/b],[d/b;-d/b],[u/b+ymax;-u/b-ymin],[],[],[xmin],[xmax])-u/b)
for i= umax:-0.1:umin
    vmin=linprog([1/(b+d) 1/(b+d)],[],[],[d -b],[-c*i*b+a*i*d],[xmin ymin],[xmax ymax])-i*(a+c)/(b+d);
    vmax=-linprog([-1/(b+d) 1/(b+d)],[],[],[d -b],[-c*i*b+a*i*d],[xmin ymin],[xmax ymax])-i*(a+c)/(b+d);
    if (size(vmin) ~=0 & size(vmax)~=0)
    for j=vmin:0.1:vmax
        jq=f3(i,j)+jq;
    end
    end
end
jf-jq
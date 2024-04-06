axis equal
n=30;
r=20;
x=100;y=100;z=0;
[x1,y1,z1] = sphere(n);
old=[x
     y
     z];
t=2*pi/200;
M=Rmatrix(t);
for i=1:1000
    new=M*old;
    surf(3*r*x1,3*r*y1,3*r*z1)
    axis([-200 200 -200 200 -100*2^0.5 100*2^0.5])
    hold on
    surf(r*x1+new(1),r*y1+new(2),r*z1+new(3));
    axis([-200 200 -200 200 -100*2^0.5 100*2^0.5])
    hold off
    old=new;
    pause(0.01)
end
function M= Rmatrix(t)
M = [cos(t),-sin(t),0
     sin(t),cos(t),0
     0,0,1];
end
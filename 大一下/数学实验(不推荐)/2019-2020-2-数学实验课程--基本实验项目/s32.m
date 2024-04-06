function r=fun()
[t,x]=ode45(@f,0:0.1:5,[2 0]);
r=x(:,1);
end
function dx=f(t,x)
dx = zeros(2,1);
dx(1)=x(2);
dx(2)=20*(1-x(1)^2)*x(2)+0.5*x(1);
end

function [x0,y0]=fun
y=@(x)(-1.*exp(x).*x.*sin(x));
l=0;r=9;minx=l;min=y(minx);
while 1
  [tminx,tmin]=fminbnd(y,l,r);
  if tminx-minx<1e-4
      break
  end
  if tmin<min
      min=tmin;minx=tminx;
  end
  l=tminx;
end
x=0:0.01:9;
z=y(x);
plot(x,-z);
x0=minx;
y0=-min;
end
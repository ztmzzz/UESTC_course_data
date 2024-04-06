y=@(x)2.*x.^3-3.*x.^2+4.*x-5;
p=[2 -3 4 -5];
roots(p)
xp=fzero(y,1)

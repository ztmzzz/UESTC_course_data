function xp=fun()
f=@(x)2*x^3-3*x^2+4*x-5;
xp=fzero(f,0);
end
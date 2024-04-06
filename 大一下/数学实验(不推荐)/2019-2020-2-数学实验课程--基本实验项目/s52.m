t(1)=5*rand;n=0;i=1;
while t(i)<=30*60
    i=i+1;
    n=n+1;
    t(i)=5*rand+t(i-1);
end
n
t
d=unifrnd(0,5,1,100);
t(1)=d(1);
for i=2:100
    t(i)=d(i)+t(i-1);
end

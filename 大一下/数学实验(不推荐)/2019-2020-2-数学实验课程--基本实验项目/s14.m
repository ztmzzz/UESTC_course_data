i=0;
for x=1:1000
    for y=1:1000
        if (x^2-100*y==x)
            i=i+1;
            a(i)=x;
            b(i)=y;
        end
    end
end
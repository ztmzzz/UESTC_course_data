
close all
%建立正多边形数据
t = 0:pi/3:2*pi;
r = 5;
x = r*cos(t);
y = r*sin(t); %产生了正多边形6个节点坐标(这里有7个，其中起点，重点重合）

x = x + 6; % 平移一下得到初始正六边形顶点坐标
y = y + 6;
tt = 2*pi/200;
P = [x
     y];
M = rotM(tt); %每次动画旋转角度都为tt
for i=1:200    
    PNew = M*P;
    P = PNew;
    
    plot(P(1,:),P(2,:),'r-')
    axis([-30 30 -30 30])
    axis equal
    pause(0.02)
end

function M= rotM(t)
%输入参数t为旋转角度
M = [cos(t),-sin(t)
     sin(t),cos(t)];
end
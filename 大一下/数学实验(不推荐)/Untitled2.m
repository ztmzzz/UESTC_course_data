syms S acc t vel
vel_robot=S*acc*t;
assume(vel == acc*t);
vel_robot = simplify(vel_robot)
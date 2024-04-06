import random

a = ["零件1", "零件2", "零件3", "零件4", "零件5"]
b = ["e1", "2021款e2", "e2升级版", "e3升级版", "元Pro", "全新元EV", "2021款唐", "2021款唐DM", "2021款唐EV", "唐DM-i", "宋PLUS EV",
     "宋Pro", "宋Pro EV", "宋MAX EV", "汉DM", "汉EV", "秦PLUS DM-i", "秦PLUS EV", "秦Pro EV超能版", "秦Pro超越版"]
c = []  # '零件1','秦PLUS DM-i'
random.seed(54161)
for i in b:
    num = random.randint(1, 3)
    choose = random.sample(range(1, 6), num)
    for n in choose:
        s = "('零件" + str(n) + "','" + i + "'),"
        c.append("'零件" + str(n) + "','" + i + "'")
        # print(s)
color = ["红", "橙", "黄", "绿", "青", "蓝", "紫"]
pai = [1.5, 2, 0.5, 3, 5]
name = ["王老菊", "王师傅", "铲车人", "视角姬", "林佳奇", "六道", "纯黑", "老番茄", "凉风", "路人甲", "路人乙", "路人丙", "路人A", "路人B", "丁真"]
for i in range(200):
    Cjin = random.randint(1, 3)
    money = random.randint(30000, 120000)
    choose = random.randint(0, 6)
    Ccolor = color[choose]
    choose = random.randint(0, 4)
    Cpai = pai[choose]
    choose = random.randint(0, len(c) - 1)
    year1 = random.randint(2015, 2020)
    month1 = random.randint(1, 12)
    day1 = random.randint(1, 28)
    s = "(" + str(i + 1) + ",'" + Ccolor + "','" + str(Cpai) + "'," + c[choose] + "," + str(money) + ",'经销商" + str(
        Cjin) + "','" + str(year1) + "-" + str(month1) + "-" + str(day1) + "'),"
    # print(s)
    choose = random.randint(0, 14)
    Cname = name[choose]
    year = random.randint(2017, 2021)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    while True:
        if year > year1:
            break
        elif year == year1:
            if month > month1:
                break
            elif month == month1:
                if day > day1:
                    break
                else:
                    day = random.randint(day1, 28)
            elif month<month1:
                month = random.randint(month1, 12)
        elif year<year1:
            year = random.randint(year1, 2021)

    s = "('经销商" + str(Cjin) + "'," + str(i + 1) + ",'" + Cname + "','" + str(year) + "-" + str(month) + "-" + str(
        day) + "'),"
    print(s)

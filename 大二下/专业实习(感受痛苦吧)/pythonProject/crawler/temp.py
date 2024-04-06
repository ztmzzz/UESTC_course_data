def getList():
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    f1 = open('学校id.txt', 'r', encoding='utf-8')
    line = f1.readline()
    line = line.strip()  # 去除换行符
    for i in range(1, 555):
        list1.append(line)
        line = f1.readline()
        line = line.strip()
    for j in range(1, 555):
        list2.append(line)
        line = f1.readline()
        line = line.strip()
    for k in range(1, 555):
        list3.append(line)
        line = f1.readline()
        line = line.strip()
    for l in range(1, 555):
        list4.append(line)
        line = f1.readline()
        line = line.strip()
    while line:
        list5.append(line)
        line = f1.readline()
        line = line.strip()
    print(list1)
    print(list2)
    print(list3)
    print(list4)
    print(list5)

    f1.close()
# Python基本语法

# 注释

​	单行注释 ：以#开头，**#** 右边的所有东西当做说明，而不是真正要执行的程序，起辅助说明作用

```python
# 我是注释，可以在里写一些功能说明之类的哦
print('hello world')
```


​	多行注释 :以三个单引号’’‘开头，三个单引号’’'结尾，注释内容放在中间

```python
'''
我是多行注释，
可以写很多很多行的功能说明
'''
print('hello world')
```



# 变量及类型

变量可以是**任意的数据类型**，在程序中用一个变量名表示

变量名<font color='red'>必须</font>是大小写英文、数字、下划线组成，且不能以数字开头

驼峰命名：JackMarry        jack_marry

```python
a = 1 # 变量a是一个整数
test_007 = 'Test_007' # 变量test_007是一个字符串
```

赋值：例如 a= “ABC”,Python解释器干了两件事

​	在内存中创建了一个"ABC"的字符串
​	在内存中创建一个名为a的变量，并把它指向"ABC"

# 关键字（标识符）

## 1.什么是关键字？

​	Python一些具有特殊功能的标示符，就是所谓的关键字，Python已经使用了，**所以不允许开发者自己定义和关键字相同名字的标示符**

## 2.查看关键字

```python
import keyword
print(keyword.kwlist)
```

## 3.关键字

```python
['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
```



# 格式化输出

## 1.什么是格式化？

​	在程序中，看到了 % 这样的占位符，这就是Python中格式化输出 【也叫制式输出】

```python
age = 10
print("我今年%d岁"%age)

age = 18
name = "xiaohu"
print("我的姓名是%s,年龄是%d"%(name,age))

```

## 2.常用的格式符号

<img src="C:\Users\Mihan\AppData\Roaming\Typora\typora-user-images\image-20210702202905521.png" alt="image-20210702202905521" style="zoom:70%;" />

## 3.特殊的输出

```python
print("aaa","bbb","ccc") # 打印输出，值之间空格隔开且不换行
print("www","baidu","com",sep=".") # 打印输出，值之间用点连接且不换行
print("hello",end="")# 打印输出，值之间不分开开且不换行
print("world",end="\t") # 打印输出，值之间用一个制表符隔开且不换行
print("python",end="\n") # 打印输出，值之间用一个换行隔开
print("end")
```

​	运行结果

```
aaa bbb ccc
www.baidu.com
helloworld	python
end
```

## 4.换行输出

​	在输出的时候，如果有 \n 那么，此时 \n 后的内容会在另外一行显示

```python
print("1234567890-------") # 会在一行显示
print("1234567890\n-------") # 一行显示1234567890，另外一行显示-------
```

## 5.输入

input()的小括号中放入的是，提示信息，用来在获取数据之前给用户的一个简单提示

input()在从键盘获取了数据以后，会存放到等号左边的变量中

Tips: **input()函数接受的输入必须是表达式**

```python
password = input("请输入密码:")
print('您刚刚输入的密码是:', password)
```

## 6.判断变量名类型

​	type()函数中的小括号中放入变量名，返回变量名的类型

```python
a=100
print(type(a))
```

## 7.运算符

![img](https://img-blog.csdnimg.cn/20200920081605443.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FaUDUxWlg=,size_16,color_FFFFFF,t_70#pic_center)

![img](https://img-blog.csdnimg.cn/20200920081605437.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FaUDUxWlg=,size_16,color_FFFFFF,t_70#pic_center)

![img](https://img-blog.csdnimg.cn/20200920081605420.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FaUDUxWlg=,size_16,color_FFFFFF,t_70#pic_center)

![img](https://img-blog.csdnimg.cn/20200920081605410.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FaUDUxWlg=,size_16,color_FFFFFF,t_70#pic_center)

![img](https://img-blog.csdnimg.cn/20200920081605387.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FaUDUxWlg=,size_16,color_FFFFFF,t_70#pic_center)

![img](https://img-blog.csdnimg.cn/20200920081605320.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1FaUDUxWlg=,size_16,color_FFFFFF,t_70#pic_center)



## 8.流程控制语句

### 1.条件判断语句

##### if分支语句：

格式化：**Pycharm里ctrl+alt+L可以一键format，好用**  【注意（QQ）热键冲突】

```python
if 要判断的条件:
	# 执行语句
	
age = 30
print ("------if判断开始------")
if age>=18:
    print ("我已经成年了")
    
print ("------if判断结束------")


# if-else
if 要判断的条件:
    # 执行语句1
else:
    # 执行语句2

age = 12
print("------if判断开始------")
if age >= 17:
    print("我已经成年了")
else:
    print("我还年轻")

print("------if判断结束------")
    
  
# 多分支if-elif-else语句
if 表达式1：
	# 执行语句1
elif 表达式2：
    # 执行语句2
elif 表达式3：
    # 执行语句3
elif 表达式n：
    # 执行语句n
else :
    # 执行语句n+1

score = 77
if score>=90 and score<=100:
    print('本次考试，等级为A')
elif score>=80 and score<90:
    print('本次考试，等级为B')
elif score>=70 and score<80:
    print('本次考试，等级为C')
elif score>=60 and score<70:
     print('本次考试，等级为D')
else: #elif可以else一起使用
     print('本次考试，等级为E')

        
# if嵌套
if 表达式1:
	# 执行语句1
	...(省略)...
    if 表达式2:
   	# 执行语句2
    ...(省略).
 
gender = 1 # 用1代表男生，0代表女生
danShen = 1 # 用1代表单身，0代表有男/女朋友
if gender == 1:
	print("是男生")
	if danShen == 1:
		print("我给你介绍一个吧？")
	else:
		print("你给我介绍一个呗？")
else:
	print("你是女生")
	print("……")

  

```



### 2. 循环语句

**for循环**

```python
for 临时变量 in 列表或者字符串等:
# 循环满足条件时执行的代码
	
# 从[0,5)区间，从0开始，到5结束，默认步进值为1，取数
for i in range(5): 
    print(i)
# 循环输出变量名的值
name = 'chengdu'
for x in name:
	print(x)
# 从[0,10)区间，从0开始，到12结束，以步进值为3取值
for a in range(0,12,3):
    print(a)
# 从数组中取出元素
a = ["aa","bb","cc","dd"]
for i in range(len(a)):
    print(i,a[i])

```

**while循环**

```python
while 表达式:
   # 执行语句

i = 0
while i<5:
    print("当前是第%d次执行循环"%(i+1))
    print("i=%d"%i)
    i+=1
    
 # while-else循环

while 表达式:
    # 执行语句1
else:
    # 执行语句2
    
count = 0
while count<5:
    print(count,"小于5")
    count+=1
 else:
    print(count,"大于或等于5")   

```



练习：打印九九乘法表

```python

```

### 3. break、continue和pass语句

​	break语句可以跳出for和while的循环体

```python
i = 0
while i<10:
    i = i+1
    print('----')
    if i==5:
        break
     print("当前i的值为%d"%i)   
print(i)
```

​	continue语句跳过当前循环，直接进入下一轮循环

```python
i = 0
while i<10:
    i = i+1
    print('----')
    if i==5:
        continue
    print("当前i的值为%d"%i)
print(i)
```

​	pass是空语句，一般用作占位语句，不做任何事情



### 4. Import

​	在Python用import 或者 from…import 来导入相应的库或者模块，俗称导包

```python
import sys

#从某个模块中导入某个函数,
from somemodule import somefunction
from somemodule import firstfunc, secondfunc,thirdfunc


import random # 引入随即库
a = random.randint(0,2) #随机生成0、1、2中的一个数字，赋值给变量a
```

练习：实现石头剪刀布

```python
# 输入  自己： input()  电脑：random         a = random.randint(0,2)     0：石头 1：剪刀 2 布

# 比较  if elif  a=1 c=0     a=1 c=2
# 输出  you sucks           winner 

```



# 核心数据类型

### 1. 字符串

​	Python中的字符串可以使用单引号、双引号和三引号(三个单引号或三个双引号)括起来,表示一个字符串

```python
# 方式一：
word = '字符串'
# 方式二：
sentence = "则会是一个句子"
# 方式三：
parapraph = """
        想没有用，要实际操作！
"""

print(word)
print(sentence)
print(parapraph)

```



| 方法                                                         | 描述                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| capitalize()                                                 | 将字符串的第一个字符转换为大写                               |
| center(width, fillchar)                                      | 返回一个指定的宽度 width 居中的字符串，fillchar 为填充的字符，默认为空格。 |
| count(str, beg= 0,end=len(string))                           | 返回 str 在 string 里面出现的次数，如果 beg 或者 end指定则返回指定范围内 str 出现的次数 |
| bytes.decode(encoding=“utf-8”,  errors=“strict”)             | Python3 中没有  decode 方法，但我们可以使用 bytes 对象的  decode() 方法来解码给定的 bytes 对象，这个  bytes 对象可以由str.encode() 来编码返回。 |
| encode(encoding=‘UTF-8’,errors=‘strict’)                     | 以 encoding 指定的编码格式编码字符串，如果出错默认报一个ValueError 的异常，除非 errors 指定的是’ignore’或者’replace |
| endswith(suffix, beg=0, end=len(string))                     | 检查字符串是否以 obj 结束，如果beg 或者 end指定则检查指定的范围内是否以 obj 结束，如果是，返回 True,否则返回 False |
| expandtabs(tabsize=8)                                        | 把字符串 string 中的  tab 符号转为空格，tab 符号默认的空格数是8 |
| find(str, beg=0, end=len(string))                            | 检测 str 是否包含在字符串中，如果指定范围 beg 和 end，则检查是否包含在指定范围内，如果包含返回开始的索引值，否则返回-1 |
| index(str, beg=0, end=len(string))                           | 跟find()方法一样，只不过如果str不在字符串中会报一个异常      |
| isalnum()                                                    | 如果字符串至少有一个字符并且所有字符都是字母或数字则返 回 True,否则返回False |
| isalpha()                                                    | 如果字符串至少有一个字符并且所有字符都是字母则返回 True, 否则返回 False |
| isdigit()                                                    | 如果字符串只包含数字则返回 True 否则返回 False…              |
| islower()                                                    | 如果字符串中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字符都是小写，则返回 True，否则返回 False |
| isnumeric()                                                  | 如果字符串中只包含数字字符，则返回 True，否则返回 False      |
| isspace()                                                    | 如果字符串中只包含空白，则返回 True，否则返回 Fals           |
| istitle()                                                    | 如果字符串是标题化的(见  title())则返回 True，否则返回 False |
| isupper()                                                    | 如果字符串中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字 符都是大写，则返回 True，否则返回 False |
| join(seq)                                                    | 以指定字符串作为分隔符，将 seq 中所有的元素(的字符串表示)合并为一个新的字符串 |
| len(string)                                                  | 返回字符串长度                                               |
| [ljust(width, fillchar])                                     | 返回一个原字符串左对齐,并使用  fillchar 填充至长度 width 的新字符串，fillchar  默认为空格。 |
| lower()                                                      | 转换字符串中所有大写字符为小写                               |
| lstrip()                                                     | 截掉字符串左边的空格或指定字符                               |
| ITmaketrans()                                                | 创建字符映射的转换表，对于接受两个参数的最简单的调用方式，第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串表示转换的目标。 |
| max(str)                                                     | 返回字符串 str 中最大的字母                                  |
| min(str)                                                     | 返回字符串 str 中最小的字母                                  |
| [replace(old, new , max])                                    | 把 将字符串中的 str1 替换成  str2,如果 max 指定，则替换不超过 max 次 |
| rfind(str,beg=0,end=len(string))                             | 类似于 find()函数，不过是从右边开始查找                      |
| rindex( str, beg=0, end=len(string))                         | 类似于 index()，不过是从右边开始                             |
| [rjust(width, fillchar])                                     | 返回一个原字符串右对齐,并使用fillchar(默认空格）填充至长度width 的新字符串 |
| rstrip()                                                     | 删除字符串字符串末尾的空格                                   |
| split(str="",  num=string.count(str)) num=string.count(str)) | 以 str 为分隔符截取字符串，如果 num 有指定值，则仅截取 num+1 个子字符串 |
| [splitlines(keepends])                                       | 按照行(’\r’, ‘\r\n’, \n’)分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为 False，不包含换行符，如果为 True，则保留换行符。 |
| startswith(substr, beg=0,end=len(string))                    | 检查字符串是否是以指定子字符串 substr 开头，是则返回 True，否则返回 False。如果beg 和 end 指定值，则在指定范围内检查 |
| [strip(chars])                                               | 在字符串上执行 lstrip()和  rstrip()                          |
| swapcase()                                                   | 将字符串中大写转换为小写，小写转换为大写                     |
| title()                                                      | 返回"标题化"的字符串,就是说所有单词都是以大写开始，其余字母均为小写(见istitle()) |
| translate(table, deletechars="")                             | 根据 str 给出的表(包含 256 个字符)转换 string  的字符, 要 过滤掉的字符放到 deletechars 参数中 |
| upper()                                                      | 转换字符串中的小写字母为大写                                 |
| zfill (width)                                                | 返回长度为 width 的字符串，原字符串右对齐，前面填充0         |
| isdecimal()                                                  | 检查字符串是否只包含十进制字符，如果是返回 true，否则返回 false |

```python
str='chengdu'
print(str) # 输出字符串
print(str[0:-1]) # 输出第一个到倒数第二个的所有字符
print(str[0]) # 输出字符串第一个字符
print(str[2:5]) # 输出从第三个开始到第五个的字符
print(str[2:]) # 输出从第三个开始后的所有字符
print(str * 2) # 输出字符串两次
print(str + '你好') # 连接字符串
print(str[:5]) # 输出第五个字母前的所有字符
print(str[0:7:2]) # [起始：终止：步长]
print('------------------------------')
print('hello\nchengdu') # 使用反斜杠(\)+n转义特殊字符
print(r'hello\npython') # 在字符串前面添加一个 r，表示原始字符串，不会发生转义

```



### 2. List ( 列表 )

**列表的定义**

```
变量名 = [元素1,元素2，元素3,....]
```

```python
# 列表的定义
namesList = ['xiaoWang','xiaoZhang','xiaoHua']

# 通过索引取出列表中的元素
print(namesList[0])
print(namesList[1])
print(namesList[2])

# 通过for循环取出列表中的元素
for name in namesList:
	print(name)

```

**注意事项：**

- 列表是写在方括号[]之间，元素之间用逗号分隔开
- 列表索引值**以0为开始值**，-1为从末尾的开始位置
- 列表中元素的类型可以不相同，它支持数字、字符串甚至可以包含列表（所谓的嵌套）
- 列表可以使用+操作符进行拼接，使用*表示重复

| 方法                                | 操作名称                   | 解释操作                                                     |
| ----------------------------------- | -------------------------- | ------------------------------------------------------------ |
| list[index]                         | 访问列表中的元素           | 通过下标直接访问列表中的元素                                 |
| list[start：end：length]            | 列表的切片                 | 使用[开始下标索引:结束下标索引 :步进值 ]，注意范围区间是"左闭右开" |
| for i in list:print(i)              | 遍历列表元素               | for循环                                                      |
| list.append(values)                 | 【增】追加数据到列表中尾部 | 将新的元素值追加到当前列表中末尾位置                         |
| list.extend(list1)                  | 【增】列表的追加           | 将其他列表的元素添加到当前列表中                             |
| list.insert(index,value)            | 【增】列表数据插入         | 根据给定索引指定位置插入元素                                 |
| list.remove(value)  del list[index] | 【删】列表的删除           | remove：移除列表中指定值的第一个匹配值。如果没找到的话，会抛异常  del ：我们通过索引删除指定位置的元素。 |
| list.pop()                          | 【删】弹出列表尾部元素     | 弹出当前列表尾部元素,相当于删除元素                          |
| list[index] = 8                     | 【改】更新列表中的数据     | 通过下标修改指定元素                                         |
| value in list  value not in list    | 【查】列表成员关系         | In  not in                                                   |
| list.index(value,start,end)         | 【查】列表成员关系         | 查找列表中是否存在指定的元素，存在返回元素的下标，找不到则报错，注意范围区间是"左闭右开" |
| list.count(value)                   | 【查】查找元素出现次数     | 统计指定元素在当前列表中出现的次数                           |
| list3 = list1 +list2                | 列表的加法操作             | +                                                            |
| list.sort()                         | 【排】列表的排序           | 将当前列表元素进行排序                                       |
| list.reverse()                      | 【排】列表的反转           | 将列表所有元素进行反转                                       |
| len()                               | 获取列表长度               | 获取当前列表长度                                             |
| max()                               | 获取列表元素最大值         | 获取列表元素最大值                                           |
| min()                               | 获取列表元素最小值         | 获取列表元素最小值                                           |
| list()                              | 其他类型对象转换成列表     | 其他类型对象转换成列表                                       |

```python
namelist = ["小张","小王","小李","qzp","wjw"]
print(namelist[0])
print(namelist[0:2:1]) # 列表切片
namelist.append("尾部") # 列表元素追加
list1 = ["list1"]
namelist.extend(list1) # 追加列表元素
namelist.insert(0,"王者") # 列表元素插入
for name in namelist:
    print(name)
del namelist[5] # 删除指定索引的元素
namelist.remove("qzp") # 删除指定元素
for name in namelist:
    print(name)
findName = input("请输入你想要查找的名字")
if findName in namelist: # 查找列表元素是否存在指定的元素
    print("恭喜你，找到你需要的姓名")
else:
    print("很遗憾，没有找到")
a = ["a","b","d","c","g","f"]
print(a.index("a", 0, 5)) # 查找列表中是否存在指定的元素，存在返回元素的下标,不存在则报错
a.reverse() # 将列表元素反转
print(a)
a.sort() # 将列表元素升序
print(a)
a.sort(reverse = Ture) # 将列表元素降序
print(len(a)) # 获取列表长度

```

##### 列表嵌套

​	一个列表中的元素又是一个列表，就是列表嵌套，说白了，就是一个二维数组

```python
# 列表嵌套的定义：
schoolNames = [['北京大学','清华大学'],['南开大学','天津大学','天津师范大学'],['山东大学','中国海洋大学']]
# 列表嵌套取出元素
print(schoolNames[0][0])
print(schoolNames[1][-1])
      
```

### 3. 元组(Tuple )

​	tuple与list相似，不同之处在于tuple的元素写在小括号里，元素之间用逗号隔开，**数据类型不可变**

```python
tupl = ()
# 判断类型
print(type(tup1))

tup2 = (50,) # 加逗号，类型为元组
print(type(tup2)) # 输出：<class 'tuple'>
tup3 = (50) # 不加逗号，类型为整型
print(type(tup3)) # 输出：<class 'int'>

元组的访问
tup1 = ('Google', 'baidu', 2000, 2020)
tup2 = (1, 2, 3, 4, 5, 6, 7 )
print ("tup1[0]: ", tup1[0])
print ("tup2[1:5]: ", tup2[1:5])

```

**元组的常用方法**

![image-20210702234153977](C:\Users\Mihan\AppData\Roaming\Typora\typora-user-images\image-20210702234153977.png)

```python
tup1 = (1,2,3,4,5)
# 增
tup2 = ("qzp","wjw")
tup3 = tup1 + tup2 # 重新创建一个新的元组
print(tup3)
# 删
del tup3 # 删除整个元组变量，不仅仅删除元组里面的元素
print(tup3) # 删除之后，打印就会报错: name 'tup3' is not defined
# 查
print(tup1[0])
print(tup2[1])
# 改
tup1[0] = 100 # 报错，不允许修改

```

​	**注意事项：**

- 定义一个只有一个元素的tuple，必须加逗号
- 定义好的元组的元素不可修改，但可以包含对象，如list
- 删除时，是删除整个元组，不是元组中的元素



### 4. 字典(dict)

​	字典是无序的对象集合，使用键值对（key-value）存储，具有极快的查找速度

```python
#变量info为字典类型
info = {'name':'班长', 'id':100, 'sex':'f', 'address':'地球亚洲中国北京'}
```

​	**字典的特点**

- 字典和列表一样，也能都存储多个数据
- 字典的每个元素由2部分组成，键:值。例如 ‘name’:‘班长’ ,'name’为键，'班长’为值
- 同一个字典中，键(key)必须是唯一的
- 键(key)必须使用不可变类型

```python
#字典的访问
info = {'name':'qzp','age':24}

print(info['name']) # 获取名字
print(info['age']) # 获取年龄
print(info.get('sex')) # 获取不存在的key，获取到空的内容，返回none,不会出现异常
print(info.get('sex','男')) #通过key获取到空的内容，可以设置默认值来返回，获取不为空的内容，则返回获取的值
```

**常用方法：**

![image-20210702234559169](C:\Users\Mihan\AppData\Roaming\Typora\typora-user-images\image-20210702234559169.png)

```python
info = {'name':'qzp','age':'24','sex':'男'}
# 查
print(info['name']) # 根据主键获取值
print(info['age'])
print(info['sex'])
for i in info: # 遍历只能拿到主键
    print(i)
print(info.keys()) # 得到所有的主键列表：dict_keys(['name', 'age', 'sex'])
print(info.values()) #得到所有的值列表：dict_values(['qzp', '24', '男'])
print(info.items()) #得到所有的项列表dict_items([('name', 'qzp'), ('age', '24'), ('sex', '男')])
# 增
newId = input("请输入你加入的id")
info['id'] = newId
print("_"*20) # 打印分割线
print('新增后遍历字典元素')
for i in info:
    print(i,info[i])
# 删
# del 
del info['id'] # 根据key删除相对应的value
print("删除后的遍历字典元素")
for i in info:
    print(i,info[i])
del info; # 删除字典
# clear :清除字典中的所有元素
info.clear(info);
# 改
info['name'] = 'wjw'
for i in info:
    print(i,info[i])
# 遍历
# 遍历所有的主键
for i in info.keys():
    print(i)
# 遍历所有的值
for i in info.values():
    print(i)
# 遍历所有的key-value
for key,value in info.items():
    print(key,value)

# 补充知识
myList = ['a','b','c','d','e','f']
for i,x in enumerate(myList): # 使用枚举函数，同时获取列表中的下标索引和下标对应的元素
    print(i+1,x)  
```



### 5. 集合(set)

​	set是一组key的集合，但不存储value

```python
#创建一个空集合
myset = set()

#定义一个集合
myset = set([1,2,3])
print(type(myset)) #输出结果：<class 'set'>
print(myset) # 输出结果：{1, 2, 3}


```

**特点：**

- 一组key的集合，但不存储value
- key不可以重复
- set是无序的，重复的元素会被自动过滤



**常用方法：**

<img src="C:\Users\Mihan\AppData\Roaming\Typora\typora-user-images\image-20210702234918476.png" style="zoom:80%;" />

```python
myset = set([1,2,3])
print(type(myset))
print(myset)

#增
set1 = set(['qzp','wjw'])
myset.update(set1)
print(myset)

myset.add('wangze')
print(myset)

# 删
myset.remove('wangze')
print(myset)

val = myset.pop()
print(val)
print(myset)

print(myset.clear())
del myset

```

### 总结

![image-20210702235026699](C:\Users\Mihan\AppData\Roaming\Typora\typora-user-images\image-20210702235026699.png)



